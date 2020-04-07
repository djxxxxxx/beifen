import asyncio

async def waiter(x):
    print("start{}".format(x))
    await asyncio.sleep(x)
    print("sleep {} seconds".format(x))


async def main():
    await asyncio.wait([waiter(4), waiter(1), waiter(2)])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
