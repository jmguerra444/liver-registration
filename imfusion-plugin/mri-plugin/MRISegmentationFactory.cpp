#include "MRISegmentationFactory.h"

#include "MRISegmentationAlgorithm.h"
#include "MRISegmentationController.h"

namespace ImFusion
{
	MRISegmentationAlgorithmFactory::MRISegmentationAlgorithmFactory()
	{
		// register the MRISegmentationAlgorithm
		registerAlgorithm<MRISegmentationAlgorithm>("SIRT;MRISegmentation Algorithm");
	}


	AlgorithmController* MRISegmentationControllerFactory::create(Algorithm* a) const
	{
		// register the MRISegmentationController for the MRISegmentationAlgorithm
		if (MRISegmentationAlgorithm* alg = dynamic_cast<MRISegmentationAlgorithm*>(a))
			return new MRISegmentationController(alg);
		return 0;
	}
}
