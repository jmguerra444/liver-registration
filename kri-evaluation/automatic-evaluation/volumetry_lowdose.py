import subprocess
import time
import datetime
import json

from utils import getData, log

data = getData()
workspace = "C://Master thesis//master//kri-evaluation//automatic-evaluation//base-lowdose.iws"
filename = "C://Master thesis//master//kri-evaluation//plugin-volumetry-lowdose.txt"

log("STARTING PROCESS {}".format(str(datetime.datetime.now())), filename)

a = 2
data["lowdose-ct"] = ["../../../Selected MR-CT data/{:03d}_SEGM/CT".format(a)]

lowdose_data = data["lowdose-ct"]

for i in lowdose_data:
    print("Now doing {}".format(i))
    log(i, filename)
    p = subprocess.Popen('ImFusionSuite "{}" Data="{}"'.format(workspace, i))
    time.sleep(100)
    p.terminate()