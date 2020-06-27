
from os.path import join, isfile, basename
from os import remove, mkdir
from os.path import isdir
from pathlib import Path


def safe_mkdir(n: str):
    Path(n).mkdir(exist_ok=True)


def safe_remove(n: str):
    # missing_ok not available in <3.8
    try:
        Path(n).unlink()
    except:
        pass


# from functools import lru_cache


from time import sleep

_LOCKFILE_SUFFIX = "~~#~~.lock"
FOLDER = "@cache"


def wait_for_lock_file(filename):
    while _lockfile_exists(filename):
        sleep(0.1)
    return


# @lru_cache()
def lockfile_path(original_file_name: str) -> str:
    return join(FOLDER, f"{basename(original_file_name)}{_LOCKFILE_SUFFIX}")


def create_lockfile(filename: str) -> str:
    safe_mkdir(FOLDER)
    open(lockfile_path(filename), "w").close()


def close_lockfile(filename: str) -> str:
    safe_mkdir(FOLDER)
    rm_path = lockfile_path(filename)
    safe_remove(rm_path)


def _lockfile_exists(filename: str) -> bool:
    return isfile(lockfile_path(filename))


def open_and_read(filename, should_wait_for_lockfile=False, mode="r"):
    safe_mkdir(FOLDER)
    if not isfile(filename):
        return None
    if should_wait_for_lockfile:
        wait_for_lock_file(filename)
    elif _lockfile_exists(filename):
        return None
    create_lockfile(filename)
    with open(filename, mode) as f:
        dx = f.read().strip()
        close_lockfile(filename)
        return dx or None


def open_and_write(filename, data, should_wait_for_lockfile=False, mode="w"):
    safe_mkdir(FOLDER)
    if should_wait_for_lockfile:
        wait_for_lock_file(filename)
    elif _lockfile_exists(filename):
        return None
    create_lockfile(filename)
    with open(filename, mode) as f:
        f.write(data)
        close_lockfile(filename)

