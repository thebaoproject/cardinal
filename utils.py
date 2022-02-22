import datetime

def handle_error(content: str):
    print(content)

def handle_time(time: str):
    """
    Convert "time string"s like 3m4s into neat datetime format

    :param times:
    :return:
    """
    timer = {
        "y": 0,
        "d": 0,
        "h": 0,
        "m": 0,
        "s": 0
    }

    buffer = ""
    for i in time:
        if i.isnumeric():
            buffer += str(i)
        elif i == "h":
            timer["h"] = int(buffer)
            buffer = ""
        elif i == "m":
            timer["m"] = int(buffer)
            buffer = ""
        elif i == "s":
            timer["s"] = int(buffer)
            buffer = ""
        elif i == "d":
            timer["d"] = int(buffer)
            buffer = ""
        elif i == "y":
            timer["y"] = int(buffer)
            buffer = ""
        

    dur = datetime.timedelta(seconds=timer["s"], minutes=timer["m"], hours=timer["h"], days=timer["d"])
    a = datetime.datetime.now() + dur
    if timer["y"] == 0:
        return a
    else:
        return datetime.datetime(a.year + timer["y"], seconds=timer["s"], minutes=timer["m"], hours=timer["h"], days=timer["d"])

