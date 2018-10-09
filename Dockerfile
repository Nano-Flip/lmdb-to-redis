FROM python:3.7-alpine3.8
LABEL maintainer="TheLamer"

# Versioning
ARG SHA

RUN \
 echo "**** install runtime packages ****" && \
 apk add --no-cache \
	libc-dev \
	curl \
        gcc && \
 echo "**** install script deps ****" && \
 pip --no-cache-dir install  \
	lmdb \
        redis && \
 echo "**** Add python script from Github ****" && \
 if [ -z ${SHA+x} ]; then \
	SHA=$(curl -sX GET "https://api.github.com/repos/Nano-Flip/lmdb-to-redis/commits/master" \
	| awk '/sha/{print $4;exit}' FS='[""]'); \
 fi && \
 mkdir -p \
        /lmdb-to-redis && \
 curl -o \
 /lmdb-to-redis/app.py -L \
	"https://raw.githubusercontent.com/Nano-Flip/lmdb-to-redis/${SHA}/app.py"

# volumes
VOLUME /nano

# Entry
CMD ["/usr/local/bin/python", "/lmdb-to-redis/app.py"]
