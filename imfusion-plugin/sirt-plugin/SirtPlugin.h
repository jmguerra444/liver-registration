#pragma once

#include <ImFusion/Base/ImFusionPlugin.h>

namespace ImFusion
{
	class AlgorithmFactory;
	class AlgorithmControllerFactory;

	/// Minimal example for defining a custom plugin for the ImFusion SDK
	class SirtPlugin : public ImFusionPlugin
	{
	public:
		SirtPlugin();
		virtual ~SirtPlugin();
		virtual const AlgorithmFactory* getAlgorithmFactory();
		virtual const AlgorithmControllerFactory* getAlgorithmControllerFactory();

	private:
		AlgorithmFactory* m_algFactory;
		AlgorithmControllerFactory* m_algCtrlFactory;
	};
}
