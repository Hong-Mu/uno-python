import asyncio

class MyClass:

    def __init__(self):
        self.c2 = MyClass2()

    async def timer_loop(self):
        cnt = 0
        task2 = None
        while True:
            cnt += 1
            print(f"[C1] 타이머 동작 중...{cnt}")
            await asyncio.sleep(1)  # 1초마다 작업 수행


            if cnt == 5:
                task2 = asyncio.create_task(self.c2.timer_loop())
            elif cnt == 10:
                task2.cancel()




class MyClass2:
    async def timer_loop(self):
        while True:
            print("[C2]타이머 동작 중...")
            await asyncio.sleep(1)  # 1초마다 작업 수행

async def main():
    c1 = MyClass()

    task1 = asyncio.create_task(c1.timer_loop())

    await asyncio.gather(task1)

if __name__ == '__main__':
    asyncio.run(main())