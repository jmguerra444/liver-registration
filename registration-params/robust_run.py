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
run_only = 56
startFrom = 0

parser = argparse.ArgumentParser()
parser.add_argument("--key", help = "Key", type = str, default = "FFD")
parser.add_argument("--timer", help = "Timer", type = int, default = 200)
args = parser.parse_args()
timer = args.timer
key = args.key

# workspace = getWorkspace("SEGMENT")
workspace = getWorkspace(key)
landmarks = getData("landmarks-markus.json")

params = getParams(key, version = -1)
grid = generateGrid(params)
grid = grid[startFrom:]

# TO RUN ALL STUDIES
grid = [generateGrid(getParams(key, version = i)) for i in [0, 1, 2]]
grid = [*grid[0], *grid[1], *grid[2]]

# ESTIMATE COMPUTATION TIME
c = 0
for p in landmarks:
    if landmarks[p].get("annotated"):
        c += 1

print("ESTIMATED COMPUTATION TIME: {} hours".format(
    len(grid) * timer * c / 3600))

# %% Setup
for parameters in grid:
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

            pr.terminate()
            # if run_only:
            #     pr.wait()
            # else:
            #     pr.terminate()
