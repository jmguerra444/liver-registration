ECHO FINE LANDMARK EVALUATION

python run.py --workspace="su_points_333.iws" ^
              --description="Substudy for number of point controls 333" ^
              --timer=180

python run.py --workspace="su_points_444.iws" ^
              --description="Substudy for number of point controls 444" ^
              --timer=360

python run.py --workspace="su_points_555.iws" ^
              --description="Substudy for number of point controls 555" ^
              --timer=600

python run.py --workspace="su_smooth_0.iws" ^
              --description="Substudy for number of point controls 444" ^
              --timer=500

python run.py --workspace="su_smooth_01.iws" ^
              --description="Substudy for number of point controls 444" ^
              --timer=500

python run.py --workspace="su_smooth_0001.iws" ^
              --description="Substudy for number of point controls 444" ^
              --timer=500

ECHO STEPS
python run.py --workspace="so_step_1.iws" ^
              --description="Substudy for number of point controls 444" ^
              --timer=500

python run.py --workspace="so_step_5.iws" ^
              --description="Substudy for number of point controls 444" ^
              --timer=360

python run.py --workspace="so_step_10.iws" ^
              --description="Substudy for number of point controls 444" ^
              --timer=500

python run.py --workspace="so_step_20.iws" ^
              --description="Substudy for number of point controls 444" ^
              --timer=500