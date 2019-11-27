import sys
import os
sys.path.append(os.path.abspath("../lib"))

import json
import os
from console import Console as con

def loadSettings(filename):
    """
    Loads configuration settings for this session from configuration.json
    """
    try:
        thisComputer = os.environ['COMPUTERNAME']
        with open(filename) as json_file:
            data = json.load(json_file)
        return data[thisComputer]
    except:
        con.printw("Not valid configuration file")
        return