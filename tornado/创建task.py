import asyncio, time

async def work(x):
    print('waiting:', x)

coroutine = work(3)
loop = asyncio.get_event_loop()

# task = asyncio.ensure_future(coroutine)
task = loop.create_task(coroutine)
print(task)

loop.run_until_complete(task)
print(task)
