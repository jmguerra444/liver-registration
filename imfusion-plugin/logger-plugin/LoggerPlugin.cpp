#include "LoggerPlugin.h"

#include "LoggerFactory.h"

// Export free factory function to instantiate plugin
#ifdef WIN32
extern "C" __declspec(dllexport) ImFusion::ImFusionPlugin* createPlugin()
{
	return new ImFusion::LoggerPlugin;
}
#else
extern "C" ImFusion::ImFusionPlugin* createPlugin()
{
	return new ImFusion::LoggerPlugin;
}
#endif


namespace ImFusion
{
	LoggerPlugin::LoggerPlugin()
	{
		m_algFactory = new LoggerAlgorithmFactory;
		m_algCtrlFactory = new LoggerControllerFactory;
	}


	LoggerPlugin::~LoggerPlugin() {}


	const ImFusion::AlgorithmFactory* LoggerPlugin::getAlgorithmFactory() { return m_algFactory; }


	const ImFusion::AlgorithmControllerFactory* LoggerPlugin::getAlgorithmControllerFactory() { return m_algCtrlFactory; }
}
