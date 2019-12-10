import logging

class Console:
    """
    Console
    ====
    
    Console ourput formater. Example:
        >>> print(FontStyle.w + "Warning: No active frommets remain. Continue?" + FontStyle.e)
    Or as static member funcions
        >>> FontStyle.printbl("this is a blue text")
        
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
    b = '\033[1m'         # BOLD
    u = '\033[4m'         # UNDERLINE
    e = '\033[0m'         # ENDC

    @staticmethod
    def printbl(myText):
        print('\033[94m', myText, '\033[0m')
    
    @staticmethod
    def printgr(myText):
        print('\033[92m', myText, '\033[0m')
    
    @staticmethod
    def printh(myText):
        print('\033[95m', myText, '\033[0m')
    
    @staticmethod
    def printw(myText):
        print('\033[93m', myText, '\033[0m')
    
    @staticmethod
    def printf(myText):
        print('\033[91m', myText, '\033[0m')
    
    @staticmethod
    def printb(myText):
        print('\033[1m', myText, '\033[0m')
    
    @staticmethod
    def printu(myText):
        print('\033[4m', myText, '\033[0m')

class Logger:
    """
    Logger
    ====
    
    Reimplementation of logging library from python, with added console prints
    """
    
    # TODO : Add summary function

    def __init__(self, filename):
        logging.basicConfig(
            filename = filename,
            format = '%(levelname)s - %(asctime)s - %(message)s',
            datefmt='%d.%m %H:%M:%S',
            level = logging.INFO)
                
    def info(self, myText, w = True):
        print(myText)
        if(w):
            logging.info(myText)
            
    def infoh(self, myText, w = True):
        Console.printgr(myText)
        if(w):
            logging.info(myText)
    
    def infoh2(self, myText, w = True):
        Console.printbl(myText)
        if(w):
            logging.info(myText)
        
    def warning(self, myText, w = True):
        Console.printw(myText)
        if(w):
            logging.warning(myText)
    
    def error(self, myText, w = True):
        Console.printf(myText)
        if (w):
            logging.error(myText)