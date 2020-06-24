# Define a new CMake project for the LinkPose plugin
project(LinkPosePlugin)
cmake_minimum_required(VERSION 3.2.0)

# Locate the ImFusion SDK.
# List required modules/plugins in the COMPONENTS section (e.g. COMPONENTS ImFusionSeg ImFusionReg).
list(APPEND CMAKE_PREFIX_PATH "C:/doseplan/externals/QT_5_7_VS2015/5.7/msvc2015_64/lib/cmake/Qt5")
find_package(ImFusionLib REQUIRED)

# Enable automatic MOC, RCC and UIC preprocessing for Qt
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)


# Define and configure the CMake target
set(Sources
    LinkPoseAlgorithm.cpp
    LinkPoseController.cpp
    LinkPoseFactory.cpp
    LinkPosePlugin.cpp
)
set(Headers
	LinkPoseAlgorithm.h
	LinkPoseController.h
	LinkPoseFactory.h
	LinkPosePlugin.h
)
set(UiSources
	LinkPoseController.ui
)

# Define target library
add_library(LinkPosePlugin SHARED ${Sources} ${UiHeaders} ${Headers})
target_include_directories(LinkPosePlugin PRIVATE
	${CMAKE_CURRENT_SOURCE_DIR}
)
# Link agains the ImFusionLib and selected modules/plugins
target_link_libraries(LinkPosePlugin PRIVATE
	ImFusionLib
)

# Define output target directories and provide instructions on how to launch
# the ImFusion Suite with the built custom plugin.
# These functions are provided by the ImFusionLib target config. 
imfusion_set_common_target_properties()
imfusion_provide_ide_instructions()

