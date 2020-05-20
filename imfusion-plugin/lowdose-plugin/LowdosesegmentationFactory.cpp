#include "LowDoseSegmentationFactory.h"

#include "LowDoseSegmentationAlgorithm.h"
#include "LowDoseSegmentationController.h"

namespace ImFusion
{
	LowDoseSegmentationAlgorithmFactory::LowDoseSegmentationAlgorithmFactory()
	{
		// register the LowDoseSegmentationAlgorithm
		registerAlgorithm<LowDoseSegmentationAlgorithm>("SIRT;LowDose Segmentation Algorithm");
	}


	AlgorithmController* LowDoseSegmentationControllerFactory::create(Algorithm* a) const
	{
		// register the LowDoseSegmentationController for the LowDoseSegmentationAlgorithm
		if (LowDoseSegmentationAlgorithm* alg = dynamic_cast<LowDoseSegmentationAlgorithm*>(a))
			return new LowDoseSegmentationController(alg);
		return 0;
	}
}
