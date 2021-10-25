import asyncio, time


async def blink(txt, period):
    for i in range(3):
        print(txt)
        await asyncio.sleep(period)

async def main():
    task1 = asyncio.create_task(blink("a", 1))
    task2 = asyncio.create_task(blink("b", 5))

    print("Attend")
    time.sleep(2)
    print("Go")
    await asyncio.gather(task1, task2, return_exceptions=False)


asyncio.run(main())