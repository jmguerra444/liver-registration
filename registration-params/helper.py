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
        "0_" : "misc",
        "n_" : "normal-linear"
    }
    return kinds.get(workspace[:2], "")
