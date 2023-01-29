import aioredis
import asyncio

redis = aioredis.from_url("redis://")


async def create():
    
    await redis.set('my-key', 'value')
    val = await redis.get('my-key')
    print(val)


async def r():
    await create()

asyncio.run(create())

#asyncio.run(create())

'''async def main():
    redis = await aioredis.create_redis(
        'redis://localhost')
    await redis.set('my-key', 'value')
    val = await redis.get('my-key')
    print(val)

    # gracefully closing underlying connection
    redis.close()
    await redis.wait_
    


if __name__ == '__main__':
    asyncio.run(main())
    asyncio.run(redis_pool())'''