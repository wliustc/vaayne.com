## MongoDB
1. database : blog
2. collection: posts, users
3. posts:
    `db.posts.ensureIndex({"source_url":1,"slug":-1}, {unique: true}})`

## Redis
```
$ wget http://download.redis.io/releases/redis-3.2.2.tar.gz
$ tar xzf redis-3.2.2.tar.gz
$ cd redis-3.2.2
$ make
```