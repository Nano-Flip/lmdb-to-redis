## Usage

```
docker run --rm -i \
  --name=lmdb-to-redis \
  -v <path to RaiBlocks>:/nano \
  -e REDIS_HOST=<redis host> \
  -e REDIS_PORT=<redis port> \
  nanoflip/lmdb-to-redis:latest
```
