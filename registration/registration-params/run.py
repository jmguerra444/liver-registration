# %% Dependencies
import os
import subprocess
import argparse
import random

from utils import getData, log, screenshot, now, absolutePath
from helper import fieldInversability, generateGrid, getSpecificPatients, setup, getSpecificGrid, paramsToString
from robust_params import getParams, getWorkspace

# RUN ALL DATASETS ONE WORKSPACE
run_only = 0    # 0 if you want to run the study in all the patients
                # <patient id> (E.G 55)

parser = argparse.ArgumentParser()
parser.add_argument("--key", help="Key", type=str, default="FFD_ADV")
parser.add_argument("--timer", help="Timer", type=int, default=300)
parser.add_argument("--location", help="Where the data is located", type = str, default = "C:/Users/jmgue/OneDrive - SurgicEye GmbH/thesis/data/Selected MR-CT data")
args = parser.parse_args()

location = args.location    # Where the data is stored in my case D:/jorge/OneDrive/OneDrive - SurgicEye GmbH/thesis/data/Selected MR-CT data
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
# params = {
#         "similarity": ["NCC"],     # Or define the parameters here NO VALUE CAN BE EMPTY, this is error prone
#         "step_size": [5],
#         "grid_size": ["6 6 6"],
#         "smoothness": [0]
#         }

## ---------   CUSTOMIZATIONS FOR THE EXPERIMENT ----------
grid = generateGrid(params)       # Generates all the combinations for the parameters to run the studies
# grid = grid[0:]                   # Change in case you want start study from some other number
grid = getSpecificGrid(key)         # Or define some list of desired combinations
landmarks = getSpecificPatients(landmarks)      # Filter to get only specific patients

# Randomly delete some in the grid
# grid = random.sample(grid, int(len(grid) * 0.2))
# grid = random.sample(grid, 20)

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
    study_id = now() + "_" + workspace[:-4] + "_" + paramsToString(parameters) + "_" + key
    study = {
        "id": study_id,
        "workspaceFile": "workspaces//{}".format(workspace),
        "description": parameters,
        "studyFolder": absolutePath("studies//in-progress//{}".format(study_id)),
        "descriptionFile": absolutePath("studies//in-progress//{}//description".format(study_id)),
        "screenshotFolder": absolutePath("studies//in-progress//{}//screenshots//".format(study_id)),
        "deformationsFolder": absolutePath("studies//in-progress//{}//deformation_fields//".format(study_id))
        }
    setup(study)

    for p in landmarks:
        # To only one
        if run_only:
            if not(run_only and int(p) == run_only):
                continue

        if landmarks[p].get("annotated"):
            print(p)
            mriPath = location + landmarks[p].get("mri-data")
            ctPath = location + landmarks[p].get("ct-data")
            points1 = landmarks[p].get("points1")
            points2 = landmarks[p].get("points2")
            fieldPath = "{}//{}.h5".format(study["deformationsFolder"], p)

            # Make sure ImFusionSuite is in the path
            c = 'ImFusionSuite_2_16_3 {} mr="{}" ct="{}" p1="{}" p2="{}" {}'.format(study["workspaceFile"],
                                                                                    mriPath,
                                                                                    ctPath,
                                                                                    points1,
                                                                                    points2,
                                                                                    parameters)

            if ("ADV" in key):
                c += ' field="{}"'.format(fieldPath)

            pr = subprocess.Popen(c)
            if run_only:
                pr.wait()
            else:
                screenshotPath = "{}//{}.png".format(study["screenshotFolder"], p)
                screenshot(screenshotPath, timer)  # Not asynchronous
                pr.terminate()

            if os.path.exists(fieldPath):
                print("Computing Jacobian")
                inv = fieldInversability(fieldPath)
                log(p + " " + str(inv), study.get("descriptionFile"))
                os.remove(fieldPath)
            else:
                print("The file does not exist")
