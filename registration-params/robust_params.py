
from helper import crop

workspace = ""
params = {}

# workspace = "gn_ffd.iws"
# params = {"similarity" : ["NCC", "MI", "SSD"],
#           "step_size" : [1, 5, 10, 15],
#           "smoothness" : [0, 0.1, 0.01, 0.001, 0.0001]
#          }

workspace = "gn_simple.iws"
params = { \
          "similarity" : ["MI", "SSD", "NCC", "LNCC"],
          "affine" : [1, 0],
          "crop_upper" : [crop(0), crop(33)], # Remove slices from the top
          "crop_lower" : [crop(0)]   # Remove slices from bottom
         }

# workspace = "gn_simple.iws"
# params = { \
#           "similarity" : ["MI", "SSD", "NCC", "LNCC"],
#           "affine" : [1, 0],
#           "crop_upper" : [crop(0), crop(33)], # Remove slices from the top
#           "crop_lower" : [crop(0)]   # Remove slices from bottom
#          }

# workspace = "gn_linear.iws"
# params = { \
#           "similarity" : ["MI"],
#           "affine" : [1],
#           "crop_upper" : [crop(0), crop(33)], # Remove slices from the top
#           "crop_lower" : [crop(0)]   # Remove slices from bottom
#          }

# params = {"similarity" : ["NCC"],
#           "affine" : [0],
#          }

def getParams():
    return params

def getWorkspace():
    return workspace