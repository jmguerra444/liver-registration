# %% Dependencies
from utils import getData, log, screenshot, now, absolutePath
from helper import setup
import time
import subprocess
import datetime
import os
import argparse
# import pdb

# Change this to run only in one set
run_only = 6
description = "Dummy study description"
workspace = "t_affine_ncc.iws"
timer = 70

# run_only = 0
# parser = argparse.ArgumentParser()
# parser.add_argument("--workspace", help = "Workspace file inside /workspaces/", type = str, default = "rigid_mi.iws")
# parser.add_argument("--description", help = "Study description", type = str, default = "Description of the study")
# parser.add_argument("--timer", help = "Timer", type = int, default = 50)
# args = parser.parse_args()
# description = args.description
# workspace = args.workspace
# timer = args.timer

# %% Setup
landmarks = getData("landmarks.json")
study_id = now()
study = {
    "id" : study_id,
    "workspaceFile" : "workspaces\\{}".format(workspace),
    "description" : description,
    "studyFolder" : absolutePath("studies\\in-progress\\{}".format(study_id)),
    "descriptionFile" : absolutePath("studies\\in-progress\\{}\\description".format(study_id)),
    "screenshotFolder" : absolutePath("studies\\in-progress\\{}\\screenshots\\".format(study_id))
    }
setup(study)

# %% Session
log("\n",study.get("descriptionFile"))
log("STARTING PROCESS {}".format(now()), study.get("descriptionFile"))
for p in landmarks :
    
    # To only one
    if run_only:
        if not(run_only and int(p) == run_only):
            continue
    
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
        screenshot(screenshotPath, timer) # Not asynchronous

        if run_only:
            process.wait()
        else:
            process.terminate()

# %%
