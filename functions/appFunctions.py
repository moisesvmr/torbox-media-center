from functions.torboxFunctions import getUserDownloads, DownloadType
from library.filesystem import MOUNT_METHOD
from library.torbox import TORBOX_API_KEY
from functions.filesystemFunctions import initializeFolders

def getAllUserDownloads():
    all_downloads = []
    for download_type in DownloadType:
        downloads, success, detail = getUserDownloads(download_type)
        if not success:
            print(f"Error fetching {download_type.value}: {detail}")
            continue
        all_downloads.extend(downloads)

def bootUp():
    print("Booting up...")
    print("Mount method:", MOUNT_METHOD)
    print("TorBox API Key:", TORBOX_API_KEY)

    initializeFolders()

    return True
