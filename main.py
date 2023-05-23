import asyncio

from screen.ScreenController import ScreenController


async def main():
    controller = ScreenController()
    pygame_task = asyncio.create_task(controller.run())

    await asyncio.gather(pygame_task)

if __name__ == '__main__':
    asyncio.run(main())


