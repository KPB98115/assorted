from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import Optional
from pydantic import BaseModel
import os, threading, uuid, asyncio, logging, time
from PIL import Image

logger = logging.getLogger(__name__)

class Status(Enum):
    SUCCESS = 0
    FAILED = 1
    PROCESS = 2

class ImageStatus(BaseModel):
    status: Status
    gridfs_id: Optional[str] = None
    error_message: Optional[str] = None
    completed_at: Optional[float] = None

class AlbumAssociationStatus(BaseModel):
    associated: bool = False
    error_message: Optional[str] = None

class Job(BaseModel):
    id: str
    src: str
    dist: str
    thumbnail_dist: str
    main_image: ImageStatus
    thumbnail: ImageStatus
    album_association: Optional[AlbumAssociationStatus] = None

    @property
    def status(self) -> Status:
        if self.main_image.status == Status.FAILED or self.thumbnail.status == Status.FAILED:
            return Status.FAILED
        elif self.main_image.status == Status.SUCCESS and self.thumbnail.status == Status.SUCCESS:
            return Status.SUCCESS
        else:
            return Status.PROCESS

    @property
    def completed_at(self) -> Optional[float]:
        if self.main_image.completed_at and self.thumbnail.completed_at:
            return max(self.main_image.completed_at, self.thumbnail.completed_at)
        return None

class Converter:
    def __init__(self, image_client=None, job_ttl_seconds: int = 3600):
        self.temp_dir = "/tmp/image_converter"
        os.makedirs(self.temp_dir, exist_ok=True)

        self.main_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="main_img")
        self.thumb_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="thumbnail")

        self.jobs = {}
        self.thread_lock = threading.Lock()
        self.image_client = image_client
        self.job_ttl_seconds = job_ttl_seconds

    def submit(self, src_path: str, filename: str, album_id: Optional[str] = None, album_client=None) -> str:
        
        base_filename = os.path.splitext(filename)[0]
        
        safe_filename = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in base_filename)
        job_id = f"{safe_filename}_{uuid.uuid4().hex[:8]}_job"

        dist_path = os.path.join(self.temp_dir, f"{job_id}.webp")
        thumbnail_path = os.path.join(self.temp_dir, f"{job_id}_thumb.webp")

        job = Job(
            id=job_id,
            src=src_path,
            dist=dist_path,
            thumbnail_dist=thumbnail_path,
            main_image=ImageStatus(status=Status.PROCESS),
            thumbnail=ImageStatus(status=Status.PROCESS)
        )

        with self.thread_lock:
            self.jobs[job_id] = job

        def _process_main():
            start_time = time.time()
            try:
                logger.info("Thread started")

                img = Image.open(src_path)

                img = self._convert_color_type(img)

                main_img = img.copy()
                main_img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)

                main_img.save(dist_path, 'WEBP', quality=100)

                if self.image_client:
                    logger.info("Starting GridFS upload")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        main_id = loop.run_until_complete(
                            self.image_client.uploadFileToBucket(dist_path, f"{filename}.webp")
                        )
                        job.main_image.gridfs_id = main_id
                    finally:
                        loop.close()

                job.main_image.status = Status.SUCCESS
                job.main_image.completed_at = time.time()

            except Exception as e:
                job.main_image.status = Status.FAILED
                job.main_image.error_message = str(e)
                job.main_image.completed_at = time.time()

            finally:
                try:
                    if os.path.exists(dist_path):
                        os.remove(dist_path)
                except Exception as e:
                    logger.error("Clean up failed")

        def _process_thumbnail():
            try:
                img = Image.open(src_path)
                
                img = self._convert_color_type(img)

                thumb_img = img.copy()
                thumb_img.thumbnail((512, 512), Image.Resampling.LANCZOS)
                
                thumb_final = Image.new('RGB', (512, 512), (255, 255, 255))
                paste_x = (512 - thumb_img.width) // 2
                paste_y = (512 - thumb_img.height) // 2

                if thumb_img.width > 512 or thumb_img.height > 512:
                    left = (thumb_img.width - 512) // 2
                    top = (thumb_img.height - 512) // 2
                    thumb_img = thumb_img.crop((left, top, left + 512, top + 512))
                    paste_x = 0
                    paste_y = 0

                thumb_final.paste(thumb_img, (paste_x, paste_y))

                thumb_final.save(thumbnail_path, 'WEBP', quality=100)

                if self.image_client:
                    while job.main_image.gridfs_id is None and job.main_image.status == Status.PROCESS:
                        time.sleep(0.1)  # poll in every 100ms

                    if job.main_image.gridfs_id:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            thumb_id = loop.run_until_complete(
                                self.image_client.uploadFileToBucket(thumbnail_path, f"thumbnail_{job.main_image.gridfs_id}.webp")
                            )
                            job.thumbnail.gridfs_id = thumb_id
                        finally:
                            loop.close()
                    else:
                        raise Exception("Main image processing failed.")

                job.thumbnail.status = Status.SUCCESS
                job.thumbnail.completed_at = time.time()

            except Exception as e:
                job.thumbnail.status = Status.FAILED
                job.thumbnail.error_message = str(e)
                job.thumbnail.completed_at = time.time()

            finally:
                try:
                    if os.path.exists(thumbnail_path):
                        os.remove(thumbnail_path)
                except Exception as e:
                    logger.info(f"Failed to clean up temp file: {e}")

        def _cleanup_source():

            main_future = self.main_executor.submit(_process_main)
            thumb_future = self.thumb_executor.submit(_process_thumbnail)

            main_future.result()
            thumb_future.result()

            if album_id and album_client and job.main_image.gridfs_id and job.thumbnail.gridfs_id:

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(
                        album_client.addImageToAlbum(album_id, job.main_image.gridfs_id, job.thumbnail.gridfs_id)
                    )

                    if result.status:
                        job.album_association = AlbumAssociationStatus(associated=True)
                    else:
                        job.album_association = AlbumAssociationStatus(associated=False, error_message=result.message)
                except Exception as e:
                    job.album_association = AlbumAssociationStatus(associated=False, error_message=str(e))
                finally:
                    loop.close()

            try:
                if os.path.exists(src_path):
                    os.remove(src_path)
            except Exception as e:
                logger.warning(f"Failed to clean up source file: {e}")

        ThreadPoolExecutor(max_workers=1).submit(_cleanup_source)

        return job_id

    def getJob(self, job_id: str) -> Optional[Job]:
        with self.thread_lock:
            return self.jobs.get(job_id)

    def cleanup_old_jobs(self):
        current_time = time.time()
        with self.thread_lock:
            jobs_to_remove = []
            for job_id, job in self.jobs.items():
                if job.completed_at and (current_time - job.completed_at) > self.job_ttl_seconds:
                    jobs_to_remove.append(job_id)

            for job_id in jobs_to_remove:
                del self.jobs[job_id]

            return len(jobs_to_remove)

    def delete_job(self, job_id: str) -> bool:
        with self.thread_lock:
            if job_id in self.jobs:
                del self.jobs[job_id]
                logger.info(f"Deleted job {job_id}")
                return True
            return False

    def shutdown(self):
        self.main_executor.shutdown(wait=True)
        self.thumb_executor.shutdown(wait=True)

    def _convert_color_type(self, img: Image.Image) -> Image.Image:
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            return background
        elif img.mode != 'RGB':
            return img.convert('RGB')
        return img