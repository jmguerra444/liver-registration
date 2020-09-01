import subprocess
import time
import datetime
import json

from utils import getData, log

data = getData()
workspace = "C://Master thesis//master//kri-evaluation//automatic-evaluation//base-ct.iws"
filename = "C://Master thesis//master//kri-evaluation//plugin-volumetry-ct.txt"

log("STARTING PROCESS {}".format(str(datetime.datetime.now())), filename)

a = 27
data["diagnostic-ct"] = ["../../../Selected MR-CT data/{:03d}_SEGM/Diagnostic".format(a)]
data["diagnostic-ct-mesh"] = ["../../../Selected MR-CT data/{:03d}_SEGM/Liver.stl".format(a)]

ct_data = data["diagnostic-ct"]
ct_mesh = data["diagnostic-mesh-ct"]

for index, i in enumerate(ct_data):
    print("Now doing {}".format(i))
    log(i, filename)
    p = subprocess.Popen('ImFusionSuite "{}" Data="{}" Mesh="{}"'.format(workspace, i, ct_mesh[index]))
    time.sleep(60)
    p.terminate()