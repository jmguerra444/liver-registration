@ECHO OFF
CALL "C:/ProgramData/Anaconda3/Scripts/activate"
CALL conda activate master-thesis
python main.py
CALL conda deactivate