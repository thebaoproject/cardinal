import youtubesearchpython.__future__ as yt

import asyncio
import json


async def do_stuffs():
    vs = yt.VideosSearch('xue hua piao piao', limit=1)
    found = await vs.next()
    print(json.dumps(found))

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(do_stuffs())
