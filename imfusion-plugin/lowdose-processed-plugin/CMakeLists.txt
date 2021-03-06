# Define a new CMake project for the LowDoseSegmentation plugin
project(LowDoseSegmentationProcessedPlugin)
cmake_minimum_required(VERSION 3.2.0)

list(APPEND CMAKE_PREFIX_PATH "C:/doseplan/externals/QT_5_7_VS2015/5.7/msvc2015_64/lib/cmake/Qt5")
# Locate the ImFusion SDK.
# List required modules/plugins in the COMPONENTS section (e.g. COMPONENTS ImFusionSeg ImFusionReg).
find_package(ImFusionLib COMPONENTS ImFusionML REQUIRED)

# Enable automatic MOC, RCC and UIC preprocessing for Qt
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)


# Define and configure the CMake target
set(Sources
    LowDoseSegmentationAlgorithm.cpp
    LowDoseSegmentationController.cpp
    LowDoseSegmentationFactory.cpp
    LowDoseSegmentationPlugin.cpp
)
set(Headers
	LowDoseSegmentationAlgorithm.h
	LowDoseSegmentationController.h
	LowDoseSegmentationFactory.h
	LowDoseSegmentationPlugin.h
)
set(UiSources
	LowDoseSegmentationController.ui
)

# Define target library
add_library(LowDoseSegmentationProcessedPlugin SHARED ${Sources} ${UiHeaders} ${Headers})
target_include_directories(LowDoseSegmentationProcessedPlugin PRIVATE
	${CMAKE_CURRENT_SOURCE_DIR}
)
# Link agains the ImFusionLib and selected modules/plugins
target_link_libraries(LowDoseSegmentationProcessedPlugin PRIVATE
	ImFusionLib
)

# Copy kernels to binary
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/model/lowdose-liver.pt" "${CMAKE_CURRENT_BINARY_DIR}/bin/Release/lowdose-liver.pt" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/model/lowdose-liver.configtxt" "${CMAKE_CURRENT_BINARY_DIR}/bin/Release/lowdose-liver.configtxt" COPYONLY)

# Define output target directories and provide instructions on how to launch
# the ImFusion Suite with the built custom plugin.
# These functions are provided by the ImFusionLib target config. 
imfusion_set_common_target_properties()
imfusion_provide_ide_instructions()
