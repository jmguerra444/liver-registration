#include "LinkPosePlugin.h"

#include "LinkPoseFactory.h"

// Export free factory function to instantiate plugin
#ifdef WIN32
extern "C" __declspec(dllexport) ImFusion::ImFusionPlugin* createPlugin()
{
	return new ImFusion::LinkPosePlugin;
}
#else
extern "C" ImFusion::ImFusionPlugin* createPlugin()
{
	return new ImFusion::LinkPosePlugin;
}
#endif


namespace ImFusion
{
	LinkPosePlugin::LinkPosePlugin()
	{
		m_algFactory = new LinkPoseAlgorithmFactory;
		m_algCtrlFactory = new LinkPoseControllerFactory;
	}


	LinkPosePlugin::~LinkPosePlugin() {}


	const ImFusion::AlgorithmFactory* LinkPosePlugin::getAlgorithmFactory() { return m_algFactory; }


	const ImFusion::AlgorithmControllerFactory* LinkPosePlugin::getAlgorithmControllerFactory() { return m_algCtrlFactory; }
}
