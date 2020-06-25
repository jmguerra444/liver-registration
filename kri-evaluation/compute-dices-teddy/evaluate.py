import subprocess
import json
import time
import pyscreenshot

def getData(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def screenshot(filename = "screenshot.png", delay_s = 0):
    time.sleep(delay_s)
    i  = pyscreenshot.grab()
    i.save(filename)

data = getData("data.json")

for i in range(len(data.get("doctor-annotation"))):
    liverP = data.get("doctor-annotation")[i]
    liverA = data.get("teddy-annotation")[i]
    p = data.get("patients")[i]
    print("Doing {}".format(p))

    c = 'ImFusionSuite workspace.iws liverA="{}" liverP="{}"'.format(liverA, liverP)
    screenshotFilename = "images/{:03d}.png".format(p)
    process = subprocess.Popen(c)
    screenshot(screenshotFilename, 20)
    process.terminate()

