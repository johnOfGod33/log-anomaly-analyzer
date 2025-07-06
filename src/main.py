import asyncio

from utils import read_logs

if __name__ == "__main__":
    asyncio.run(read_logs("events.log"))
