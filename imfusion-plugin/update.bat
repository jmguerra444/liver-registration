cd "C:\Master thesis\master\imfusion-plugin"
taskkill /IM ImFusionSuite.exe /T /F

cd registration-plugin
cmake --build build --config Release
cd ..

cd mri-plugin
cmake --build build --config Release
cd ..

cd lowdose-plugin
cmake --build build --config Release
cd ..

cd logger-plugin
cmake --build build --config Release
cd ..

xcopy /y "C:\Master thesis\master\imfusion-plugin\registration-plugin\build\bin\Release\RegistrationPlugin.dll" "C:\Program Files\ImFusion\ImFusion Suite\Suite\plugins\RegistrationPlugin.dll"
xcopy /y "C:\Master thesis\master\imfusion-plugin\mri-plugin\build\bin\Release\MRISegmentationPlugin.dll" "C:\Program Files\ImFusion\ImFusion Suite\Suite\plugins"
xcopy /y "C:\Master thesis\master\imfusion-plugin\lowdose-plugin\build\bin\Release\LowDoseSegmentationPlugin.dll" "C:\Program Files\ImFusion\ImFusion Suite\Suite\plugins"
xcopy /y "C:\Master thesis\master\imfusion-plugin\logger-plugin\build\bin\Release\LoggerPlugin.dll" "C:\Program Files\ImFusion\ImFusion Suite\Suite\plugins"

runas /savecred /user:jmguerra444@hotmail.com "ImFusionSuite.exe"
pause