import asyncio

import modules.music_engine as msc


async def main():
    result = await msc.search("ppap", n=2)
    print(msc.clean_result(result[0]))


asyncio.run(main())
