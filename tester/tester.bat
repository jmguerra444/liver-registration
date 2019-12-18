@ECHO OFF
CALL "C:/ProgramData/Anaconda3/Scripts/activate"
CALL conda activate master-thesis
START pythonw main.py
EXIT