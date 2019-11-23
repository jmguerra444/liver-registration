# Use my libs

import logging
import visual as vs
from formater import FontStyle as fs

# Viewer examples
def testViewer():
    from numpy import random
    A = random.rand(100,100,100)
    vs.viewer(A)

# Logger example
def testLogger():
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')

def testFormater():
    fs.printbl("This is a blue text")

# testViewer()
# testLogger()
testFormater()