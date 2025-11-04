from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
import os, threading, uuid

class Status(Enum):
    SUCCESS = 0
    FAILED = 1
    PROCESS = 2

class Job(BaseModel):
    id: UUID
    src: str
    dist: str
    status: Status

class Converter:
    def __init__(self):
        self.temp_dir = ""
        os.makedirs(self.temp_dir, exist_ok=True)
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.jobs = {}
        self.thread_lock = threading.Lock()

    def submit(self, src_path) -> str:
        job_id = uuid.uuid4().hex
        src_path = ""
        dist_path = os.path.join(self.temp_dir, f"{job_id}.webp")

        job = Job(id=job_id, src=src_path, dist=dist_path, status=Status.PROCESS)

        with self.thread_lock:
            self.jobs[job_id] = job
        
        def _process():
            try:
                self._convert_to_webp(src_path, dist_path)
                job.status = Status.SUCCESS
            except Exception as e:
                job.status = Status.FAILED
        
        self.executor.submit(_process)
        return job_id

    def getJob(self, job_id: str) -> Optional[Job]:
        with self.thread_lock:
            return self.jobs.get(job_id)

    def shutdown(self):
        # Wait all process to finish
        self.executor.shutdown(wait=True)

    def _convert_to_webp(src: str, dist: str):
        pass