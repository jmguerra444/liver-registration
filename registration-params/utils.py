import json
import time
import pyscreenshot
import os
from datetime import datetime

def absolutePath(relativePath):
    cwd = os.getcwd()
    path = os.path.join(cwd, relativePath)
    return path

def getData(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def log(msg, filename):
    with open(filename, "a") as t:
        print(msg)
        t.write(msg)
        t.write("\n")

def screenshot(filename = "screenshot.png", delay_s = 0):
    time.sleep(delay_s)
    i  = pyscreenshot.grab()
    i.save(filename)

def now():
    time_ = datetime.now()
    time_str = time_.strftime("%m%d%H%M%S")
    return time_str
