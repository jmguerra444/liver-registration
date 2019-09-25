import json
import os

def loadSettings():
    
    thisComputer = os.environ['COMPUTERNAME']
    with open("configuration.json") as json_file:
        data = json.load(json_file)
    
    return data[thisComputer]

def overflowNumber(value, increment, maxValue, minValue = 0):
    """
        Returns the new new value after increment.
    """
    newValue = value + increment
    if (newValue > maxValue):
        newValue = minValue + newValue - maxValue
        
    return newValue

def calmpNumber(value, maxValue, minValue = 0):
    
    if (maxValue > minValue):
        if (value >= maxValue):
            return maxValue
        if (value <= minValue):
            return minValue
        return value
    else:
        raise NameError("minValue > maxValue")
    return

class CF:
    """
    CF (ConsoleFormat)
    ------
    Console ourput formater. Example:
        >>> print(CF.w + "Warning: No active frommets remain. Continue?" + CF.e)
        
    `blue : OKBLUE`
    `green : OKGREEN`
    `h : HEADER`
    `w : OKWARNING`
    `f : FAIL`
    `e : ENDC`
    `b : BOLD`
    `u : UNDERLINE`

    Stolen from : https://stackoverflow.com/a/287944/7474885
    """
    blue = '\033[94m'     # OKBLUE
    green = '\033[92m'    # OKGREEN
    h = '\033[95m'        # HEADER
    w = '\033[93m'        # OKWARNING
    f = '\033[91m'        # FAIL
    e = '\033[0m'         # ENDC
    b = '\033[1m'         # BOLD
    u = '\033[4m'         # UNDERLINE
