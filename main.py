from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import os
from functions.appFunctions import bootUp, getMountMethod
from functions.filesystemFunctions import runFuse


if __name__ == "__main__":
    bootUp()
    mount_method = getMountMethod()

    if mount_method == "strm":
        scheduler = BlockingScheduler()
    elif mount_method == "fuse":
        scheduler = BackgroundScheduler()
    else:
        print("Invalid mount method. Exiting...")
        exit(1)

    print("\nPress Ctrl+{} to exit".format("Break" if os.name == "nt" else "C"))

    try:
        if mount_method == "strm":
            scheduler.start()
        elif mount_method == "fuse":
            scheduler.start()
            runFuse([])
    except (KeyboardInterrupt, SystemExit):
        pass