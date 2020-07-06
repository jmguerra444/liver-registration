from utils import getData, log, screenshot, now, absolutePath
from shutil import copy
import os

def setup(study):
    # Make dirs
    os.makedirs(study.get("screenshotFolder"), exist_ok = True)
    
    # Add description
    log(study.get("workspaceFile"), study.get("descriptionFile"))
    log(study.get("description"), study.get("descriptionFile"))

    # Copy workspacefile
    copy(study.get("workspaceFile"), study.get("studyFolder"))


def kind(workspace):
    kinds = {
        "td" : "thesis-deformable",
        "tl" : "thesis-linear",
        "tf" : "thesis-linear-deformable",
        "0_" : "misc",
        "n_" : "normal-linear",
        "su" : "sub-study",
        "so" : "sub-study-optimizer"
    }
    return kinds.get(workspace[:2], "")

def filterLandmarks(landmarks, best):
    
    new_landmarks = {}
    for p in landmarks:
        if (int(p) in best):
            new_landmarks[p] = landmarks[p]       
    
    return new_landmarks