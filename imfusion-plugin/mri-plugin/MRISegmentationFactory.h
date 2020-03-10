/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/Base/AlgorithmControllerFactory.h>
#include <ImFusion/Base/AlgorithmFactory.h>

namespace ImFusion
{
	class Algorithm;

	/// AlgorithmFactory for MRISegmentation plugin
	class MRISegmentationAlgorithmFactory : public AlgorithmFactory
	{
	public:
		MRISegmentationAlgorithmFactory();
	};

	/// AlgorithmControllerFactory for MRISegmentation plugin
	class MRISegmentationControllerFactory : public AlgorithmControllerFactory
	{
	public:
		virtual AlgorithmController* create(Algorithm* a) const;
	};
}
