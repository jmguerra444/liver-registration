DEL /Q build
MKDIR build
CD build
cmake .. -G "Visual Studio 14 2015 Win64"
CD ..
PAUSE