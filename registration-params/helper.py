from utils import getData, log, screenshot, now, absolutePath
from shutil import copy
import os
import itertools

def generateGrid(d):
    result = []
    
    for similarity in d["similarities"]:
        p1 = 'similarity={} '.format(similarity)
        
        for step_size in d["step_sizes"]:
            p2 = 'step_size={} '.format(step_size)
            
            result.append(p1 + p2)
    return result

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
    
    if not best:
        return landmarks
    
    new_landmarks = {}
    for p in landmarks:
        if (int(p) in best):
            new_landmarks[p] = landmarks[p]       
    
    return new_landmarks