from utils import log
logger = "logger.log"
file_ = open('C:\\Users\\Jorgue Guerra\\AppData\\Roaming\\ImFusion\\ImFusion Suite\\ImFusionSuite.log', 'r') 

def parseDices():
    Lines = file_.readlines() 
    for line in Lines:
        if ("[SIRT][LOGGER] ../../../" in line) or ("Dice similarity coefficient" in line):
            log(line, logger)

parseDices()