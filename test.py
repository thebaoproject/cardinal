import sched
import time


def some_fucking_func(useless):
    print(f"blablablabla\n{useless}")


async def main():
    print("on")
    now = time.time()
    task = sched.scheduler(time.time(), time.sleep)
    task.enter(now + 5, some_fucking_func, ("nevergonnagive",))
    await task.run()
    print("Execution preparation")
    for i in range(1, 10):
        print(i)
        time.sleep(1)


if __name__ == "__main__":
    print("exec")
    main()
    print("exed")
    time.sleep(1000)
