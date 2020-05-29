#include "LowDoseSegmentationPlugin.h"

#include "LowDoseSegmentationFactory.h"

// Export free factory function to instantiate plugin
#ifdef WIN32
extern "C" __declspec(dllexport) ImFusion::ImFusionPlugin* createPlugin()
{
	return new ImFusion::LowDoseSegmentationPlugin;
}
#else
extern "C" ImFusion::ImFusionPlugin* createPlugin()
{
	return new ImFusion::LowDoseSegmentationPlugin;
}
#endif


namespace ImFusion
{
	LowDoseSegmentationPlugin::LowDoseSegmentationPlugin()
	{
		m_algFactory = new LowDoseSegmentationAlgorithmFactory;
		m_algCtrlFactory = new LowDoseSegmentationControllerFactory;
	}


	LowDoseSegmentationPlugin::~LowDoseSegmentationPlugin() {}


	const ImFusion::AlgorithmFactory* LowDoseSegmentationPlugin::getAlgorithmFactory() { return m_algFactory; }

	const ImFusion::AlgorithmControllerFactory* LowDoseSegmentationPlugin::getAlgorithmControllerFactory() { return m_algCtrlFactory; }
}
