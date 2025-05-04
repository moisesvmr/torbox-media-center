import os
from library.filesystem import MOUNT_PATH
import shutil

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
