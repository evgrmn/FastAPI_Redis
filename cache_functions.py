import aioredis
import json

redis = aioredis.from_url("redis://redis")


async def cache_create(name, data):
    await redis.set(name, json.dumps(data))


async def cache_delete_cascade(name):
    key_list = await redis.keys(name)
    if key_list:
        await redis.delete(*key_list)


async def cache_delete(name):
    await redis.delete(name)


async def cache_update(name, data):
    key_list = await redis.keys(f"*{name}")
    if key_list:
        name = key_list[0]
        res = json.loads(await redis.get(name))
        res.update(data)
        await cache_create(name, res)


async def cache_get(name):
    key_list = await redis.keys(f"*{name}")
    if key_list:
        name = key_list[0]
        res = await redis.get(name)
        if res:
            return json.loads(await redis.get(name))
        else:
            return None
    return None