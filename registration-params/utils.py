import json
import time
import pyscreenshot

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