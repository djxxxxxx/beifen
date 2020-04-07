import asyncio, time

now = lambda: time.time()

async def work(x):
    print('waiting', x)

start = now()

loop = asyncio.get_event_loop()
loop.run_until_complete(work(3))
print('TIME:', (now()-start))
