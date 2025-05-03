from apscheduler.schedulers.blocking import BlockingScheduler
import os

if __name__ == "__main__":
    scheduler = BlockingScheduler()

    print("Press Ctrl+{} to exit".format("Break" if os.name == "nt" else "C"))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass