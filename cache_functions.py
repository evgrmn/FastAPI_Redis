import aioredis
import json

redis = aioredis.from_url("redis://")


async def cache_create(name, data):    
    await redis.set(name, json.dumps(data))


async def cache_delete(name):
    await redis.delete(name)


async def cache_update(name, data):
    res = await cache_get(name)
    res.update(data)
    await cache_create(name, res)


async def cache_get(name):
    res = await redis.get(name)
    if res:
        return json.loads(await redis.get(name))
    else:
        return None