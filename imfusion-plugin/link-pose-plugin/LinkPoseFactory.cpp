#include "LinkPoseFactory.h"

#include "LinkPoseAlgorithm.h"
#include "LinkPoseController.h"

namespace ImFusion
{
	LinkPoseAlgorithmFactory::LinkPoseAlgorithmFactory()
	{
		// register the LinkPoseAlgorithm
		registerAlgorithm<LinkPoseAlgorithm>("SIRT;LinkPose algorithm");
	}


	AlgorithmController* LinkPoseControllerFactory::create(Algorithm* a) const
	{
		// register the LinkPoseController for the LinkPoseAlgorithm
		if (LinkPoseAlgorithm* alg = dynamic_cast<LinkPoseAlgorithm*>(a))
			return new LinkPoseController(alg);
		return 0;
	}
}
