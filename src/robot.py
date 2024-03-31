import asyncio
import sys

async def start_counter(start_number=0):
    number = start_number
    try:
        while True:
            print(number)
            number += 1
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Робот остановлен.")

if __name__ == "__main__":
    start_number = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    asyncio.run(start_counter(start_number))
