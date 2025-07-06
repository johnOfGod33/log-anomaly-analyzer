import asyncio


async def read_logs(file):
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            print(line)
            await asyncio.sleep(2)
