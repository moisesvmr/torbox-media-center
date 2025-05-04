from apscheduler.schedulers.blocking import BlockingScheduler
import os
from functions.appFunctions import bootUp, getAllUserDownloads



if __name__ == "__main__":
    bootUp()
    scheduler = BlockingScheduler()

    print("\nPress Ctrl+{} to exit".format("Break" if os.name == "nt" else "C"))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass