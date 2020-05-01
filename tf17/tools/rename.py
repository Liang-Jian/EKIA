import os
import time


def batch_rename():
    path = "/Users/bithup/Desktop/capture_set/"
    suffix = ""
    filelist = os.listdir(path)
    for files in filelist:
        timec = str(time.time()).replace(".", "")
        old = os.path.join(path, files)
        new = os.path.join(path, files.replace(".", "_"+timec+"."))
        os.rename(old, new)


if __name__ == "__main__":
    batch_rename()
