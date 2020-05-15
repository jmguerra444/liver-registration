import subprocess
import time
import datetime
import json

from utils import getData, log

data = getData()
workspace = "C://Master thesis//master//kri-evaluation//automatic-evaluation//base-mri.iws"
filename = "C://Master thesis//master//kri-evaluation//plugin-volumetry-mri.txt"

log("STARTING PROCESS {}".format(str(datetime.datetime.now())), filename)

mri_data = data["diagnostic-mr"]
mesh_data = data["diagnostic-mr-mesh"]

for index, i in enumerate(mri_data):
    print("Now doing {}".format(i))
    log(i, filename)
    p = subprocess.Popen('ImFusionSuite "{}" Data="{}" Mesh="{}"'.format(workspace, i, mesh_data[index]))
    p.wait()