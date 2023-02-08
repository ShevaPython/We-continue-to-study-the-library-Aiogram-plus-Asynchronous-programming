import asyncio

"""
~Lessons_1

Asyncio

- Библиотека для сощдания асинхроных програм,для концепции асинхроного програмирования!
- Библиотека aiogram  являеться асинхроной библиотекой
- Результатом вызова асинхроной функции являеться обьект coroutine
- asyncio.run() метод для вызова асинхронной функции
- aasyncio.sleep(3) функция засыпает
- await - оживать
- asyncio.create_task() регестрация  задачь для полноценного конкурунтного кода
- Practice

"""


async def send_hello() -> None:
    await asyncio.sleep(3)
    print("Hello")


async def send_by() -> None:
    await asyncio.sleep(1)
    print("By")


# print(send_hello()) <coroutine object send_hello at 0x7f1d2ebee5e0>
async def main():
    task1 = asyncio.create_task(send_hello())
    task2 = asyncio.create_task(send_by())
    await task1
    await task2

asyncio.run(main())