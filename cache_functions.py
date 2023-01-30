import aioredis
import json

redis = aioredis.from_url("redis://")


async def cache_create(name, data):
    print('create', name, data)  
    await redis.set(name, json.dumps(data))
    #a = await redis.keys('*0*')
    #print(a)
    #if a:
    #    await redis.delete(*a)
    #for key in redis.scan_iter("Menu*"):
    #    print(key)

async def cache_delete_cascade(name):
    print('cache_delete_cascade', name)
    key_list = await redis.keys(name)
    print('------------', key_list)
    if key_list:
        await redis.delete(*key_list)

async def cache_delete(name):
    print('cache_delete', name)
    await redis.delete(name)


async def cache_update(name, data):
    key_list = await redis.keys(f"*{name}")
    if key_list:
        name = key_list[0]
        res = json.loads(await redis.get(name))
        #print(res)
        res.update(data)
        await cache_create(name, res)


async def cache_get(name):

    '''a = await redis.keys('*Menu_165_SubMenu_100*')

    l = await redis.mget(*a)

    print(l)'''
    key_list = await redis.keys(f"*{name}")
    #print(name)
    #print(key_list)
    if key_list:
        #print('(key_list', key_list[0])
        name = key_list[0]
        res = await redis.get(name)
        #print(res)
        if res:
            return json.loads(await redis.get(name))
        else:
            return None
    return None


#async 