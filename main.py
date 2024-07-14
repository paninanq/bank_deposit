from Bank import TerminalCom
import asyncio


async def main():
    while True:
        while True:
            try:
                answer = input('Хотите подобрать вклад? (Ответьте да или нет): ').strip().lower()
                assert answer in ["да", "нет"]
                break
            except AssertionError:
                print("Данные некорректны.")
                continue
        if answer == 'да':
            await TerminalCom.community()
        else:
            break


if __name__ == "__main__":
    asyncio.run(main())
