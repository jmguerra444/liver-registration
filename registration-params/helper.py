from utils import getData, log, screenshot, now, absolutePath
from shutil import copy
import os
import itertools

def generateGrid(d):
    result = []
    
    key = lambda x : list(d.keys())[x]
    
    p0 = p1 = p2 = p3 = p4 = ''
    l = len(d)

    for a0 in d[key(0)]:
        p0 = '{}={} '.format(key(0), a0)
        if l == 1 : result.append(p0)
        
        if l > 1:
            for a1 in d[key(1)]:
                p1 = '{}={} '.format(key(1), a1)
                if l == 2 : result.append(p0 + p1)

                if l > 2:
                    for a2 in d[key(2)]:
                        p2 = '{}={} '.format(key(2), a2)
                        if l == 3 : result.append(p0 + p1 + p2)

                        if l > 3:
                            for a3 in d[key(3)]:
                                p3 = '{}={} '.format(key(3), a3)
                                if l == 4 : result.append(p0 + p1 + p2 + p3)
                            
                                if l > 4:
                                    for a4 in d[key(4)]:
                                        p4 = '{}={} '.format(key(4), a4)
                                        result.append(p0 + p1 + p2 + p3 + p4)                            
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
        "so" : "sub-study-optimizer",
        "gn" : "generic-studies"
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

def paramsToString(params):
    params = params.replace(" ", "_")
    params = params.replace("=", "_")
    return params