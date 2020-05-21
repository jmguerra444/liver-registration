#include "RegistrationFactory.h"

#include "RegistrationAlgorithm.h"
#include "RegistrationController.h"

namespace ImFusion
{
	RegistrationAlgorithmFactory::RegistrationAlgorithmFactory()
	{
		// register the RegistrationAlgorithm
		registerAlgorithm<RegistrationAlgorithm>("SIRT;Registration algorithm");
	}


	AlgorithmController* RegistrationControllerFactory::create(Algorithm* a) const
	{
		// register the RegistrationController for the RegistrationAlgorithm
		if (RegistrationAlgorithm* alg = dynamic_cast<RegistrationAlgorithm*>(a))
			return new RegistrationController(alg);
		return 0;
	}
}
