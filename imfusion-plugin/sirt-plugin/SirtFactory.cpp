#include "SirtFactory.h"

#include "SirtAlgorithm.h"
#include "SirtController.h"

namespace ImFusion
{
	SirtAlgorithmFactory::SirtAlgorithmFactory()
	{
		// register the SirtAlgorithm
		registerAlgorithm<SirtAlgorithm>("Sirt;Sirt algorithm");
	}


	AlgorithmController* SirtControllerFactory::create(Algorithm* a) const
	{
		// register the SirtController for the SirtAlgorithm
		if (SirtAlgorithm* alg = dynamic_cast<SirtAlgorithm*>(a))
			return new SirtController(alg);
		return 0;
	}
}
