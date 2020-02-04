@ECHO OFF
CALL "C:/ProgramData/Anaconda3/Scripts/activate"
CALL conda activate
START pythonw main.py
EXIT