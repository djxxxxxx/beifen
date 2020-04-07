import asyncio, time

async def work(x):
    print('waiting:', x)
    return 'Done after {}s'.format(x)

def callback(future):
    print('Callback:', future.result)

corouttine = work(3)
loop = asyncio.get_event_loop()
task = loop.create_task(cotoutine)
