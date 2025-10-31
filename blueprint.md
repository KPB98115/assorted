# Album backend system

# Tech stack

Lang: Python 3.10

API framework: Fastapi

in-memory database: Mongo

Environment: Docker-compose

Named volume to store image persistently

## Endpoint and feature:

1. POST /album/create (name) → status, album_snapshot
   1. If album id exist, return false with message
2. POST /album/get (album_id) → status, album_snapshot
3. POST /album/delete (album_id) → status, message
   1. If album id not exist, return fail with message
4. POST /album/image/upload (album_id, image) → status, job_id
   1. If image size over 1920x1080 pixel, return fail
   2. If image media format is not jpg, jpeg, png, webp, heif, heic, avif (need third party library support decode).
   3. Return job_id instead of image_id, image still in process.
5. POST /album/image/delete (album_id, image_id) → status, message
   1. Delete image and thumbnail as well
   2. If either album_id or image_id not exist, return fail
6. PSOT /album/image/get (album_id, image_id) → status, image
   1. If either album_id or image_id not exist, return fail
7. POST /album/thumbnail/get (thumbnail_id) → status, thumbnail
   1. If thumbnail_id not exist, check album_id and image_id, if both exist, create a new thumbnail. Otherwise return fail

Payload property:

1. album_id: UUID
2. album_name: str
3. image_id: UUID
4. image_name: str
5. thumbnail_id: str
6. job_id: str

## Restriction

1. Large image file over 50M
2. Image width and height over 1920x1080 pixel

## Note

1. Offload the image encoding process to a queue.
2. /album/image/upload should return a job id at first place, /album/image/get should return job_id if it still in queue, otherwise return streaming image.
3. Stream the file in Mongo instead of buffer the image

## Model:

```python
class Album:
	id: UUID
	name: str
	create_date: Datetime
	content: list[Image]

class Album_snapshot(Album):
	content: list[Image.id]

class Image:
	id: UUID
	name: str
	create_date: Datetime
	thumbnail: Thumbnail

class Thumbnail:
	id: str (Album.id + Image.id)

class Job:
	id: Image.id + 'job'

```

# Frontend album design

1. After upload the image, use that image as thumbnail and normal image temporary while upload and convert is processing.
