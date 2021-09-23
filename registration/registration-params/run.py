# %% Dependencies
import time
import subprocess
import datetime
import os
import argparse

from utils import getData, log, screenshot, now, absolutePath
from helper import setup, filterLandmarks, generateGrid, paramsToString, crop, moveLandmarks
from robust_params import getParams, getWorkspace

# RUN ALL DATASETS ONE WORKSPACE
run_only = 6    # 0 if you want to run the study in all the patients
                # <patient id> (E.G 55)
startFrom = 0   # Change this in case you want to start the whole study from some patient (expects an index)

parser = argparse.ArgumentParser()
parser.add_argument("--key", help = "Key", type = str, default = "LOAD")
parser.add_argument("--timer", help = "Timer", type = int, default = 200)
parser.add_argument("--location", help= "Where the data is located", type = str, default = "D:/jorge/OneDrive/OneDrive - SurgicEye GmbH/thesis/data/Selected MR-CT data")
args = parser.parse_args()

location = args.location    # Where the data is stored in my case D:\jorge\OneDrive\OneDrive - SurgicEye GmbH\thesis\data\Selected MR-CT data
timer = args.timer          # How much time (seconds) should wait before stating the next registration
key = args.key              # What kind of study should be run
                            # Available options are:
                            # "LOAD"            Just loads the data with the landmarks
                            # "SEGMENT"         Load the data and segment
                            # "SIMPLE"          Load, segment and perform rigid registration using image data
                            # "LINEAR"          Load, segment and perform linear registration using masks
                            # "FFD"             Load, segment and perform deformable registration using masks

workspace = getWorkspace(key)
landmarks = getData("landmarks.json")
params = getParams(key)             # Use this function to get all the parameters available for the particular grid
                                    # Inspect this function to check the available params per study
# params = {\
#         "similarity" : ["NCC"],     # Or define the parameters here NO VALUE CAN BE EMPTY, this is error prone
#         "step_size" : [5],
#         "grid_size" : ["6 6 6"],
#         "smoothness" : [0]
#         }

grid = generateGrid(params)         # Generates all the combinations for the parameters to run the studies
grid = grid[startFrom:]

# ESTIMATE COMPUTATION TIME
# This is a rough approximation, it does not consider cases where only one study is run
c = 0
for p in landmarks:
    if landmarks[p].get("annotated"):
        c += 1
print("ESTIMATED COMPUTATION TIME: {} hours".format(
    len(grid) * timer * c / 3600))

# %% Setup
for parameters in grid:
    study_id = now() + "_" + workspace[:-4]  + "_" + paramsToString(parameters)
    study = {
        "id" : study_id,
        "workspaceFile" : "workspaces\\{}".format(workspace),
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
            mriPath = location + landmarks[p].get("mri-data")
            ctPath = location + landmarks[p].get("ct-data")
            points1 = landmarks[p].get("points1")
            points2 = landmarks[p].get("points2")

            # Make sure ImFusionSuite is in the path
            c = 'ImFusionSuite {} mr="{}" ct="{}" p1="{}" p2="{}" {}'.format(study["workspaceFile"],
                                                                        mriPath,
                                                                        ctPath,
                                                                        points1,
                                                                        points2,
                                                                        parameters)

            pr = subprocess.Popen(c)
            if run_only:
                pr.wait()
            else:
                screenshotPath = "{}\\{}.png".format(study["screenshotFolder"], p)
                screenshot(screenshotPath, timer) # Not asynchronous
                pr.terminate()
