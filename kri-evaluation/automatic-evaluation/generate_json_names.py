from utils import getData, log

logger = "logger.log"
data = getData()

log("LOW DOSE DATA", logger)
for i in range(1, 104):
    log("\"../../../Selected MR-CT data/{:03d}_SEGM/CT\",".format(i), logger)

log("MRI DATA", logger)
for i in range(1, 104):
    if i in data["mri-patients"]:
        log("\"../../../Selected MR-CT data/{:03d}_SEGM/Diagnostic\",".format(i), logger)

log("CT DATA", logger)
for i in range(1, 104):
    if i in data["ct-patients"]:
        log("\"../../../Selected MR-CT data/{:03d}_SEGM/Diagnostic\",".format(i), logger)