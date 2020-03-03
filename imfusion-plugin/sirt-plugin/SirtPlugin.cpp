#include "SirtPlugin.h"

#include "SirtFactory.h"

// Export free factory function to instantiate plugin
#ifdef WIN32
extern "C" __declspec(dllexport) ImFusion::ImFusionPlugin* createPlugin()
{
	return new ImFusion::SirtPlugin;
}
#else
extern "C" ImFusion::ImFusionPlugin* createPlugin()
{
	return new ImFusion::SirtPlugin;
}
#endif


namespace ImFusion
{
	SirtPlugin::SirtPlugin()
	{
		m_algFactory = new SirtAlgorithmFactory;
		m_algCtrlFactory = new SirtControllerFactory;
	}


	SirtPlugin::~SirtPlugin() {}


	const ImFusion::AlgorithmFactory* SirtPlugin::getAlgorithmFactory() { return m_algFactory; }

	const ImFusion::AlgorithmControllerFactory* SirtPlugin::getAlgorithmControllerFactory() { return m_algCtrlFactory; }
}
