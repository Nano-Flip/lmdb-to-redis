#!/usr/bin/env python
# -*- coding: utf-8 -*-
import lmdb
import redis
import random
import os

# App variables
rhost = os.environ['REDIS_HOST']
rport = os.environ['REDIS_PORT']
blocks = []
dbs = ['change','open','receive','send','state']

# Redis connection info
rc = redis.StrictRedis(
        host=rhost,
        port=rport,
        db=0)

# Convert binary arrays into hex strings
def bin2hex(s):
  assert isinstance(s, bytes)
  return s.hex().upper()

# Loop through the Nano DBs and add blocks to in memory list
for dbname in dbs:
  env = lmdb.Environment(
          '/nano/data.ldb',
          subdir=False,
          max_dbs=16,
          readonly=True,
          lock=False)
  db = env.open_db(dbname.encode())
  with env.begin(write=False) as tx:
    cur = tx.cursor(db)
    cur.first()
    for key, value in cur:
      blocks.append(bin2hex(key))
  cur.close()
  env.close()

# Shuffle the list to reduce race conditions when clustering
random.shuffle(blocks)

# To prevent locking redis we need to do individual calls for the block hashes
for block in blocks:
  if rc.exists(block) is False:
    rc.set(block,0)
