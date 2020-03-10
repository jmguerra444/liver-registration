#include "MRISegmentationPlugin.h"

#include "MRISegmentationFactory.h"

// Export free factory function to instantiate plugin
#ifdef WIN32
extern "C" __declspec(dllexport) ImFusion::ImFusionPlugin* createPlugin()
{
	return new ImFusion::MRISegmentationPlugin;
}
#else
extern "C" ImFusion::ImFusionPlugin* createPlugin()
{
	return new ImFusion::MRISegmentationPlugin;
}
#endif


namespace ImFusion
{
	MRISegmentationPlugin::MRISegmentationPlugin()
	{
		m_algFactory = new MRISegmentationAlgorithmFactory;
		m_algCtrlFactory = new MRISegmentationControllerFactory;
	}


	MRISegmentationPlugin::~MRISegmentationPlugin() {}


	const ImFusion::AlgorithmFactory* MRISegmentationPlugin::getAlgorithmFactory() { return m_algFactory; }

	const ImFusion::AlgorithmControllerFactory* MRISegmentationPlugin::getAlgorithmControllerFactory() { return m_algCtrlFactory; }
}
