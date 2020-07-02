# %% Dependencies
from utils import getData, log, screenshot, now, absolutePath
from helper import setup, kind, filterLandmarks
import time
import subprocess
import datetime
import os
import argparse
# import pdb

bestLandmarks = [25,  36,  39,  41,  46,  55,  62,  70,  80,  80,  86,  93,  94,  96,  98,  103]

# Change this to run only in one set
run_only = 8
description = "Dummy study"
workspace = "tf_rigid_ffd_test.iws"
timer = 120

# run_only = 0
# parser = argparse.ArgumentParser()
# parser.add_argument("--workspace", help = "Workspace file inside /workspaces/", type = str, default = "n_rigid_mi.iws")
# parser.add_argument("--description", help = "Study description", type = str, default = "Description of the study")
# parser.add_argument("--timer", help = "Timer", type = int, default = 50)
# args = parser.parse_args()
# description = args.description
# workspace = args.workspace
# timer = args.timer

# %% Setup

landmarks = getData("landmarks.json")
study_id = workspace[:-4] + "_" + now()
study = {
    "id" : study_id,
    "workspaceFile" : "workspaces\\{}\\{}".format(kind(workspace), workspace),
    "description" : description,
    "studyFolder" : absolutePath("studies\\in-progress\\{}".format(study_id)),
    "descriptionFile" : absolutePath("studies\\in-progress\\{}\\description".format(study_id)),
    "screenshotFolder" : absolutePath("studies\\in-progress\\{}\\screenshots\\".format(study_id))
    }
setup(study)

# For only selected landmarks study
landmarks = filterLandmarks(landmarks, bestLandmarks)

# %% Session
log("\n",study.get("descriptionFile"))
log("STARTING PROCESS {}".format(now()), study.get("descriptionFile"))
for p in landmarks :
    
    # To only one
    if run_only:
        if not(run_only and int(p) == run_only):
            continue

    # Run above
    if (int(p) < 0):
        continue

    # Run until
    if (int(p) > 1000):
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
        screenshot(screenshotPath, timer) # Not asynchronous

        if run_only:
            process.wait()
        else:
            process.terminate()
