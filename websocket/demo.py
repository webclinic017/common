#!/usr/bin/env python3
# async.py

import asyncio

async def count():
    print("11")
    await asyncio.sleep(1)
    print("12")

async def count2():
    print("21")
    await asyncio.sleep(1)
    print("22")
    
async def count3():
    print("31")
    await asyncio.sleep(1)
    print("32")

async def main():
    await asyncio.gather(count(), count2(), count3())

asyncio.run(main())