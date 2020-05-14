import subprocess
import time
import datetime
import json

workspace = "C://Master thesis//master//kri-evaluation//workspaces//base.iws"

def log(msg):
    filename = "C://Master thesis//master//kri-evaluation//plugin-volumetry-lowdose.txt"
    with open(filename, "a") as t:
        t.write(msg)
        t.write("\n")

log("STARTING PROCESS {}".format(str(datetime.datetime.now())))

with open("data.json") as json_file:
    data = json.load(json_file)

lowdose_data = data["lowdose-ct"]

for i in lowdose_data:
    print("Now doing {}".format(i))
    log(i)
    p = subprocess.Popen('ImFusionSuite "{}" Data="{}"'.format(workspace, i))
    time.sleep(60)
    p.terminate()