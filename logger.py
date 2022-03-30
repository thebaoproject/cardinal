# Yes, I implement my own logger algorithm,
import datetime
import inspect
import os


LOG = []

__FORMAT = "{color}[{time} {level}] {file}:{line}: "

__MIN_LEVEL = 0

COLOR_BLACK = "\N{ESC}[30m"
COLOR_RED = "\N{ESC}[31m"
COLOR_GREEN = "\N{ESC}[32m"
COLOR_YELLOW = "\N{ESC}[33m"
COLOR_BLUE = "\N{ESC}[34m"
COLOR_MAGENTA = "\N{ESC}[35m"
COLOR_CYAN = "\N{ESC}[36m"
COLOR_WHITE = "\N{ESC}[37m"
COLOR_RESET = " \N{ESC}[0m"

DEBUG = 2
SUCCESS = 1
INFO = 0
WARNING = -1
ERROR = -2
FUCKED = -3

N2LV = {
    "2": "DEBUG",
    "1": "SUCCESS",
    "0": "INFO",
    "-1": "WARNING",
    "-2": "ERROR",
    "-3": "FUCKED"
}
LV2CL = {
    "2": COLOR_WHITE,
    "1":  COLOR_GREEN,
    "0":  COLOR_CYAN,
    "-1": COLOR_YELLOW,
    "-2": COLOR_RED,
    "-3": COLOR_MAGENTA
}


def _log(filename: str, line: int, level: int, *message: str):
    ct = datetime.datetime.now()
    time = f"{ct.hour}:{ct.minute}:{ct.second}"
    if level > __MIN_LEVEL:
        return
    print(
        __FORMAT.format(
            file=os.path.relpath(filename),
            time=time,
            color=LV2CL[str(level)],
            line=line,
            level=N2LV[str(level)]
        ),
        *message,
        sep=""
    )
    LOG.append(
        __FORMAT.format(
            file=os.path.relpath(filename),
            time=time,
            color="",
            line=line,
            level=N2LV[str(level)]
        ) +
        "".join(message)
    )


def _get_info():
    prop = inspect.getframeinfo(inspect.stack()[2][0])
    return prop.filename, prop.lineno


def set_min_level(level: int):
    global __MIN_LEVEL
    __MIN_LEVEL = level


def debug(*message: str):
    """do stuffs"""
    a = _get_info()
    _log(a[0], a[1], DEBUG, *message)


def info(*message: str):
    """do stuffs"""
    a = _get_info()
    _log(a[0], a[1], INFO, *message)


def success(*message: str):
    """do stuffs"""
    a = _get_info()
    _log(a[0], a[1], SUCCESS, *message)


def warning(*message: str):
    """do stuffs"""
    a = _get_info()
    _log(a[0], a[1], WARNING, *message)


def error(*message: str):
    """do stuffs"""
    a = _get_info()
    _log(a[0], a[1], ERROR, *message)


def fucked(*message: str):
    """do stuffs"""
    a = _get_info()
    _log(a[0], a[1], FUCKED, *message)
