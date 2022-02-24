from functions.music import find_video
import asyncio


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(find_video("rickroll", 1))
    print(result)


if __name__ == "__main__":
    main()
