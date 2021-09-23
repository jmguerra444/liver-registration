
from helper import crop

def getParams(key, version = 0):
    params = {}
    if (key == "SIMPLE"):
        params = { \
                "similarity" : ["MI", "SSD", "NCC", "LNCC"],
                "affine" : [0, 1],
                "crop_upper" : [crop(0), crop(33)], # Remove slices from the top
                "crop_lower" : [crop(0)]   # Remove slices from bottom
                }

    if (key == "LINEAR"):
        params = { \
                "similarity" : ["MI", "SSD", "NCC", "LNCC"],
                "affine" : [0, 1],
                }

    if (key == "FFD"):
        if (version == -1):
            # Test params
            params = {\
                    "similarity" : ["NCC"],
                    "step_size" : [5],
                    "grid_size" : ["6 6 6"],
                    "smoothness" : [0]
                    }

        if (version == 0):
            # FFD 1st study
            params = {\
                    "similarity" : ["MI", "SSD", "NCC", "LNCC"],
                    "step_size" : [1, 5, 10, 15],
                    "grid_size" : ["3 3 3", "4 4 4", "5 5 5"],
                    "smoothness" : [0, 0.1, 0.01, 0.001]
                    }

        if (version == 1):
            ## FFD 2nd study
            params = {\
                    "similarity" : ["MI", "SSD", "NCC"],
                    "step_size" : [1, 5, 10, 15],
                    "grid_size" : ["6 6 6"],
                    "smoothness" : [0, 0.01, 0.001]
                    }

        if (version == 2):
            # FFD 3rd study
            params = {\
                    "similarity" : ["NCC", "SSD", "MI"],
                    "step_size" : [1, 5, 10, 15],
                    "grid_size" : ["7 7 5"],
                    "smoothness" : [0, 0.01, 0.001]
                    }
    return params

def getWorkspace(key):
    workspace = ""
    if (key == "SEGMENT"):
        workspace = "0_basic.iws"
    if (key == "SIMPLE"):
        workspace = "gn_simple.iws"
    if (key == "LINEAR"):
        workspace = "gn_linear.iws"
    if (key == "FFD"):
        workspace = "gn_ffd.iws"
    return workspace