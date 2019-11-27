# Use my libs

import logging
import visual as vs
import console as con

# Viewer examples
def testViewer():
    from numpy import random
    A = random.rand(100,100,100)
    vs.viewer(A)

def testLogger():
    logger = con.Logger("Log.log")
    logger.info("This is writen in a log file", True)

def testConsole():
    con.Console.printbl("This is blue text")

testViewer()
testLogger()
testConsole()