/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/Base/AlgorithmControllerFactory.h>
#include <ImFusion/Base/AlgorithmFactory.h>

namespace ImFusion
{
	class Algorithm;

	/// AlgorithmFactory for Sirt plugin
	class SirtAlgorithmFactory : public AlgorithmFactory
	{
	public:
		SirtAlgorithmFactory();
	};

	/// AlgorithmControllerFactory for Sirt plugin
	class SirtControllerFactory : public AlgorithmControllerFactory
	{
	public:
		virtual AlgorithmController* create(Algorithm* a) const;
	};
}
