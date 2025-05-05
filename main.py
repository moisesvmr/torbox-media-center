from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from functions.appFunctions import bootUp, getMountMethod, getAllUserDownloadsFresh
from functions.filesystemFunctions import runFuse, unmountFuse
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.getLogger("httpx").setLevel(logging.WARNING)

if __name__ == "__main__":
    bootUp()
    mount_method = getMountMethod()

    if mount_method == "strm":
        scheduler = BlockingScheduler()
    elif mount_method == "fuse":
        scheduler = BackgroundScheduler()
    else:
        logging.error("Invalid mount method specified.")
        exit(1)

    user_downloads = getAllUserDownloadsFresh()

    scheduler.add_job(
        getAllUserDownloadsFresh,
        "interval",
        hours=3,
        id="get_all_user_downloads_fresh",
    )

    try:
        logging.info("Starting scheduler and mounting...")
        if mount_method == "strm":
            scheduler.start()
        elif mount_method == "fuse":
            scheduler.start()
            runFuse()
    except (KeyboardInterrupt, SystemExit):
        if mount_method == "fuse":
            unmountFuse()
        pass