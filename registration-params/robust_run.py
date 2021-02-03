# %% Dependencies
import time
import subprocess
import datetime
import os
import argparse

from utils import getData, log, screenshot, now, absolutePath
from helper import setup, kind, filterLandmarks, generateGrid, paramsToString, crop, moveLandmarks
from robust_params import getParams, getWorkspace


# RUN ALL DATASETS ONE WORKSPACE
run_only = 0
timer = 60

params = getParams()
workspace = getWorkspace()

# %% Setup
grid = generateGrid(params)
for parameters in grid:

    landmarks = getData("landmarks-markus.json")
    study_id = workspace[:-4]  + "_" + paramsToString(parameters) + now()
    study = {
        "id" : study_id,
        "workspaceFile" : "workspaces\\{}\\{}".format(kind(workspace), workspace),
        "description" : parameters,
        "studyFolder" : absolutePath("studies\\in-progress\\{}".format(study_id)),
        "descriptionFile" : absolutePath("studies\\in-progress\\{}\\description".format(study_id)),
        "screenshotFolder" : absolutePath("studies\\in-progress\\{}\\screenshots\\".format(study_id))
        }
    setup(study)

    log("\n",study.get("descriptionFile"))
    log("STARTING PROCESS {}".format(now()), study.get("descriptionFile"))
    for p in landmarks:
        # To only one
        if run_only:
            if not(run_only and int(p) == run_only):
                continue

        if landmarks[p].get("annotated"):
            log("Doing " + p, study.get("descriptionFile"))
            mriPath = landmarks[p].get("mri-data") 
            ctPath = landmarks[p].get("ct-data")
            points1 = landmarks[p].get("points1")
            points2 = landmarks[p].get("points2")

            # points1 = moveLandmarks(points1, upper_limit)   # for the CT
            c = 'ImFusionSuite {} mr="{}" ct="{}" p1="{}" p2="{}" {}'.format(study["workspaceFile"], 
                                                                        mriPath,
                                                                        ctPath,
                                                                        points1,
                                                                        points2,
                                                                        parameters)
            
            pr = subprocess.Popen(c)
            screenshotPath = "{}\\{}.png".format(study["screenshotFolder"], p)
            screenshot(screenshotPath, timer) # Not asynchronous

            if run_only:
                pr.wait()
            else:
                pr.terminate()

# %%
