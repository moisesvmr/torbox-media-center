import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class MountMethods(Enum):
    strmfiles = "strm"
    symlink = "symlink"

MOUNT_METHOD = os.getenv("MOUNT_METHOD", MountMethods.strmfiles.value)
assert MOUNT_METHOD in [method.value for method in MountMethods], "MOUNT_METHOD is not set correctly in .env file"

MOUNT_PATH = os.getenv("MOUNT_PATH", "./torbox")