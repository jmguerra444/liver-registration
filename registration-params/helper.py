from utils import getData, log, screenshot, now, absolutePath
import os

def setup(study):
    # Make dirs
    os.makedirs(study.get("screenshotFolder"), exist_ok = True)
    
    # Add description
    log(study.get("workspaceFile"), study.get("descriptionFile"))
    log(study.get("description"), study.get("descriptionFile"))