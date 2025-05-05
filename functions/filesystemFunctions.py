import os
# from library.filesystem import MOUNT_PATH
import shutil
import fuse
from fuse import Fuse
import stat
import errno


MOUNT_PATH = "./torbox"
if not hasattr(fuse, '__version__'):
    raise RuntimeError("your fuse-python doesn't know of fuse.__version__, probably it's too old.")

fuse.fuse_python_api = (0, 2)

def initializeFolders():
    """
    Initialize the necessary folders for the application.
    """
    folders = [
        MOUNT_PATH,
        os.path.join(MOUNT_PATH, "movies"),
        os.path.join(MOUNT_PATH, "series"),
    ]

    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)

def generateFolderPath(data: dict):
    """
    Takes in a user download and returns the folder path for the download.

    Series (Year)/Season XX/Title SXXEXX.ext
    Movie (Year)/Title (Year).ext

    """
    root_folder = data.get("metadata_rootfoldername", None)
    metadata_foldername = data.get("metadata_foldername", None)

    if data.get("metadata_mediatype") == "series":
        if not metadata_foldername:
            return None
        folder_path = os.path.join(
            root_folder,
            metadata_foldername,
        )
    elif data.get("metadata_mediatype") == "movie":
        folder_path = os.path.join(
            root_folder
        )

    elif data.get("metadata_mediatype") == "anime":
        if not metadata_foldername:
            return None
        folder_path = os.path.join(
            root_folder,
            metadata_foldername,
        )
    else:
        folder_path = os.path.join(
            root_folder
        )
    return folder_path

def generateStremFile(file_path: str, url: str, type: str, file_name: str):
    if file_path is None:
        return
    full_path = os.path.join(MOUNT_PATH, type, file_path)

    os.makedirs(full_path, exist_ok=True)
    with open(f"{full_path}/{file_name}.strm", "w") as file:
        file.write(url)
