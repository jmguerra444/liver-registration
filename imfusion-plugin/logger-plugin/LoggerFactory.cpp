#include "LoggerFactory.h"

#include "LoggerAlgorithm.h"
#include "LoggerController.h"

namespace ImFusion
{
	LoggerAlgorithmFactory::LoggerAlgorithmFactory()
	{
		// register the LoggerAlgorithm
		registerAlgorithm<LoggerAlgorithm>("SIRT;Logger(dummy)");
	}


	AlgorithmController* LoggerControllerFactory::create(Algorithm* a) const
	{
		// register the LoggerController for the LoggerAlgorithm
		if (LoggerAlgorithm* alg = dynamic_cast<LoggerAlgorithm*>(a))
			return new LoggerController(alg);
		return 0;
	}
}
