/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/Base/AlgorithmControllerFactory.h>
#include <ImFusion/Base/AlgorithmFactory.h>

namespace ImFusion
{
	class Algorithm;

	/// AlgorithmFactory for Logger plugin
	class LoggerAlgorithmFactory : public AlgorithmFactory
	{
	public:
		LoggerAlgorithmFactory();
	};

	/// AlgorithmControllerFactory for Logger plugin
	class LoggerControllerFactory : public AlgorithmControllerFactory
	{
	public:
		virtual AlgorithmController* create(Algorithm* a) const;
	};
}
