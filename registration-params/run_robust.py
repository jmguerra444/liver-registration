# %% Dependencies
from utils import getData, log, screenshot, now, absolutePath
from helper import setup, kind, filterLandmarks, generateGrid
import time
import subprocess
import datetime
import os
import argparse

selectedVolumes = []

# RUN ALL DATASETS ONE WORKSPACE
run_only = 0
description = ""
workspace = "td_ffd_generic.iws"
timer = 100

# params = {"similarities" : ["NCC", "MI", "SSD"],
#           "step_sizes" : [1, 5, 10, 15],
#           "smoothness" : [0, 0.1, 0.01, 0.001, 0.0001]
#          }

params = {"similarities" : ["NCC"],
          "step_sizes" : [5],
          "smoothness" : [0.01]
         }

grid = generateGrid(params)

# %% Setup
for parameters in grid:

    landmarks = getData("landmarks-markus.json")
    study_id = workspace[:-4] + "_" + now()
    study = {
        "id" : study_id,
        "workspaceFile" : "workspaces\\{}\\{}".format(kind(workspace), workspace),
        "description" : parameters,
        "studyFolder" : absolutePath("studies\\in-progress\\{}".format(study_id)),
        "descriptionFile" : absolutePath("studies\\in-progress\\{}\\description".format(study_id)),
        "screenshotFolder" : absolutePath("studies\\in-progress\\{}\\screenshots\\".format(study_id))
        }
    setup(study)

    # For only selected landmarks study
    landmarks = filterLandmarks(landmarks, selectedVolumes)
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
            c = 'ImFusionSuite {} mr="{}" ct="{}" p1="{}" p2="{}" {}'.format(study["workspaceFile"], 
                                                                        mriPath, 
                                                                        ctPath, 
                                                                        points1, 
                                                                        points2,
                                                                        parameters)
            
            process = subprocess.Popen(c, shell = True)
            screenshotPath = "{}\\{}.png".format(study["screenshotFolder"], p)
            screenshot(screenshotPath, timer) # Not asynchronous

            if run_only:
                process.wait()
            else:
                process.terminate()

# %%
