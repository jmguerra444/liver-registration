import subprocess
import time
import pyscreenshot

def screenshot(filename = "screenshot.png", delay_s = 0):
    time.sleep(delay_s)
    i  = pyscreenshot.grab()
    i.save(filename)

patients = [
            "006", 
            "007", 
            "013", 
            "017", 
            "020", 
            "021",
            "025",
            "030",
            "036",
            "037",
            "040",
            "065",
            ]

patients = ["006"]

for p in patients:
    lowdose = "C:/Users/Jorgue Guerra/OneDrive - SurgicEye GmbH/thesis/data/Selected MR data/{}/LOWDOSE-CT".format(p)
    gt = "C:/Users/Jorgue Guerra/OneDrive - SurgicEye GmbH/thesis/data/Selected MR data/{}/ws_ct/Liver.stl".format(p)
    print(lowdose)

    c = 'ImFusionSuite workspace.iws ct="{}" gt="{}"'.format(lowdose, gt)

    screenshotPath = "screenshots/{}.png".format(p)
    process = subprocess.Popen(c)
    screenshot(screenshotPath, 60)
    # process.terminate()