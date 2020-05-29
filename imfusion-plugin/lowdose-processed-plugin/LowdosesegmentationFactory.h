/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/Base/AlgorithmControllerFactory.h>
#include <ImFusion/Base/AlgorithmFactory.h>

namespace ImFusion
{
	class Algorithm;

	/// AlgorithmFactory for LowDoseSegmentation plugin
	class LowDoseSegmentationAlgorithmFactory : public AlgorithmFactory
	{
	public:
		LowDoseSegmentationAlgorithmFactory();
	};

	/// AlgorithmControllerFactory for LowDoseSegmentation plugin
	class LowDoseSegmentationControllerFactory : public AlgorithmControllerFactory
	{
	public:
		virtual AlgorithmController* create(Algorithm* a) const;
	};
}
