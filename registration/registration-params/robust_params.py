
from helper import crop

def getParams(key, params = {}):

    if (key == "SIMPLE"):
        params = {
                "similarity" : ["MI", "SSD", "NCC", "LNCC"],
                "affine" : [0, 1],
                "crop_upper" : [crop(0), crop(33)], # Remove slices from the top
                "crop_lower" : [crop(0)]   # Remove slices from bottom
                }

    if (key == "LINEAR"):
        params = {
                "similarity" : ["MI", "SSD", "NCC", "LNCC"],
                "affine" : [0, 1],
                }

    if (key == "FFD" or key == "FFD_ADV"):
        params = {
                "similarity" : ["MI", "SSD", "NCC", "LNCC"],
                "step_size" : [1, 5, 10, 15],
                "grid_size" : ["3 3 3", "4 4 4", "5 5 5", "6 6 6", "7 7 5"],
                "smoothness" : [0, 0.1, 0.01, 0.001]
                }

    if (key == "FFD_ADV_SIMPLE"):
        params = {
                "similarity" : ["MI", "SSD", "NCC", "LNCC"],
                "step_size" : [5, 10, 15],
                "grid_size" : ["5 5 5", "6 6 6", "7 7 5"],
                "smoothness" : [0, 0.001, 0.01]
                }

    if (key == "DEA_ADV"):
        params = {"parameter" : [""]}

    return params

def getWorkspace(key):
    workspace = ""
    if (key == "LOAD"):
        workspace = "load.iws"
    if (key == "SEGMENT"):
        workspace = "segment.iws"
    if (key == "SIMPLE"):
        workspace = "register_simple.iws"
    if (key == "LINEAR"):
        workspace = "register_linear.iws"
    if (key == "FFD_ADV_SIMPLE"):
        workspace = "register_ffd_adv_simple.iws"
    if (key == "FFD"):
        workspace = "register_ffd.iws"
    if (key == "FFD_ADV"):
        workspace = "register_ffd_adv.iws"
    if (key == "DEA_ADV"):
        workspace = "register_deamon_adv.iws"
    return workspace