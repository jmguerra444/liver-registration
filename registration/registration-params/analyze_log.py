logFile = "C:/Users/Jorgue Guerra/AppData/Roaming/ImFusion/ImFusion Suite/ImFusionSuite.log"

with open(logFile) as f:
    lines = [line.rstrip() for line in f]

catchLinesWith = [
    "[Workspace] Algorithm Registration;Image Registration",
    "_SEGM/CT/"
]

result = []

for l in lines:
    for c in catchLinesWith:
        if c in l:
            result.append(l)
            print(l)
