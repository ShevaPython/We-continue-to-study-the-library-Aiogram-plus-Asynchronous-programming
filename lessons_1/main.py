import asyncio


async def count_time():
    n = 0
    while True:
        await asyncio.sleep(1)
        n += 1
        if n % 3 != 0:
            print(F"Прошло {n} секунд")


async def last_3_second():
    n = 0
    while True:
        n += 3
        await asyncio.sleep(3)
        print(F"Прошло еще {n} секунды")


async def main():
    task1 = asyncio.create_task(count_time())
    task2 = asyncio.create_task(last_3_second())
    await task1
    await task2


if __name__ == "__main__":
    asyncio.run(main())
