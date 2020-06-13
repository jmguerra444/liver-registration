# %% Dependencies
from utils import getData, log, screenshot, now, absolutePath
from helper import setup
import time
import subprocess
import datetime
import os

# %% Setup
logger = "logger.log"
landmarks = getData("landmarks.json")

description = input("What's the description os this experiment?")
study_id = now()
study = {
    "id" : study_id,
    "workspaceFile" : "workspaces\\rigid_ncc.iws",
    "description": description,
    "descriptionFile" : absolutePath("studies\\{}\\description".format(study_id)),
    "screenshotFolder" : absolutePath("studies\\{}\\screenshots\\".format(study_id))
    }
setup(study)

# %% Session
log("\n",study.get("descriptionFile"))
log("STARTING PROCESS {}".format(now()), study.get("descriptionFile"))
for p in landmarks :
    
    # Stop condition
    if (int(p) < 0):
        continue

    if landmarks[p].get("annotated"):
        log("Doing " + p, study.get("descriptionFile"))
        mriPath = landmarks[p].get("mri-data") 
        ctPath = landmarks[p].get("ct-data")
        points1 = landmarks[p].get("points1")
        points2 = landmarks[p].get("points2")
        c = 'ImFusionSuite {} mr="{}" ct="{}" p1="{}" p2="{}"'.format(study["workspaceFile"], 
                                                                      mriPath, 
                                                                      ctPath, 
                                                                      points1, 
                                                                      points2)
        
        process = subprocess.Popen(c)
        screenshotPath = "{}\\{}.png".format(study["screenshotFolder"], p)
        screenshot(screenshotPath, 50) # Not asynchronous
        process.terminate()
        # process.wait()


# %%
