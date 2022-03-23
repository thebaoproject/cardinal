import asyncio
import logger
import translations

if __name__ == "__main__":
    logger.set_min_level(logger.DEBUG)
    loop = asyncio.new_event_loop()
    a = loop.run_until_complete(translations.translate("hello world", target_language="vi"))
    print(a)
