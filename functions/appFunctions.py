from functions.torboxFunctions import getUserDownloads, DownloadType
from library.filesystem import MOUNT_METHOD, MOUNT_PATH
from library.torbox import TORBOX_API_KEY
from functions.filesystemFunctions import initializeFolders
import logging

def getAllUserDownloads():
    all_downloads = []
    for download_type in DownloadType:
        downloads, success, detail = getUserDownloads(download_type)
        if not success:
            logging.error(f"Error fetching {download_type.value}: {detail}")
            continue
        all_downloads.extend(downloads)

def bootUp():
    logging.debug("Booting up...")
    logging.info("Mount method: %s", MOUNT_METHOD)
    logging.info("Mount path: %s", MOUNT_PATH)
    logging.info("TorBox API Key: %s", TORBOX_API_KEY)
    initializeFolders()

    return True

def getMountMethod():
    return MOUNT_METHOD

def getMountPath():
    return MOUNT_PATH