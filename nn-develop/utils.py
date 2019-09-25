import json
import os

def loadSettings():
    
    thisComputer = os.environ['COMPUTERNAME']
    with open("env-settings.json") as json_file:
        data = json.load(json_file)
    
    return data[thisComputer]
