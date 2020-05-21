#include "RegistrationPlugin.h"

#include "RegistrationFactory.h"

// Export free factory function to instantiate plugin
#ifdef WIN32
extern "C" __declspec(dllexport) ImFusion::ImFusionPlugin* createPlugin()
{
	return new ImFusion::RegistrationPlugin;
}
#else
extern "C" ImFusion::ImFusionPlugin* createPlugin()
{
	return new ImFusion::RegistrationPlugin;
}
#endif


namespace ImFusion
{
	RegistrationPlugin::RegistrationPlugin()
	{
		m_algFactory = new RegistrationAlgorithmFactory;
		m_algCtrlFactory = new RegistrationControllerFactory;
	}


	RegistrationPlugin::~RegistrationPlugin() {}


	const ImFusion::AlgorithmFactory* RegistrationPlugin::getAlgorithmFactory() { return m_algFactory; }


	const ImFusion::AlgorithmControllerFactory* RegistrationPlugin::getAlgorithmControllerFactory() { return m_algCtrlFactory; }
}
