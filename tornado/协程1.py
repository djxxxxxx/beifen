import asyncio
import time
import random

# async def print_num(num):
#     print(num)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(
#     asyncio.wait([
#         print_num(num) for num in range(10)
#     ])
# )
# loop.close()

# async def waiter(name):
#     for _ in range(4):
#         time_to_sleep = random.randint(1, 3) / 4
#         time.sleep(time_to_sleep)
#         print(
#             "{} waited {} seconds"
#             "".format(name, time_to_sleep)
#         )
#
# async def main():
#     await asyncio.wait([waiter("foo"), waiter("bar")])
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     loop.close()

async def waiter(name):
    for _ in range(4):
        time_to_sleep = random.randint(1, 3) / 4
        await asyncio.sleep(time_to_sleep)
        print(
            "{} waited {} seconds"
            "".format(name, time_to_sleep)
        )

async def main():
    await asyncio.wait([waiter("foo"), waiter("bar")])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
