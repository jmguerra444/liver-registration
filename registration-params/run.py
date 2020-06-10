# p1 is tpoints
# p2 is wpoints
from utils import getData, log, screenshot
import time
import subprocess
import datetime

logger = "logger.log"
landmarks = getData("landmarks.json")

log("STARTING PROCESS {}".format(str(datetime.datetime.now())), logger)
for p in landmarks:

    if (p!="011"):
        pass
        continue

    if landmarks[p].get("annotated"):
        log("Doing " + p, logger)
        mriPath = landmarks[p].get("mri-data") 
        ctPath = landmarks[p].get("ct-data")
        points1 = landmarks[p].get("points1")
        points2 = landmarks[p].get("points2")
        c = 'ImFusionSuite ws.iws mr="{}" ct="{}" p1="{}" p2="{}"'.format(mriPath, ctPath, points1, points2)
        
        process = subprocess.Popen(c)
        screenshotPath = "screenshots/{}.png".format(p)
        screenshot(screenshotPath, 5)
        process.wait()
