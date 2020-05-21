/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/Base/AlgorithmControllerFactory.h>
#include <ImFusion/Base/AlgorithmFactory.h>

namespace ImFusion
{
	class Algorithm;

	/// AlgorithmFactory for Registration plugin
	class RegistrationAlgorithmFactory : public AlgorithmFactory
	{
	public:
		RegistrationAlgorithmFactory();
	};

	/// AlgorithmControllerFactory for Registration plugin
	class RegistrationControllerFactory : public AlgorithmControllerFactory
	{
	public:
		virtual AlgorithmController* create(Algorithm* a) const;
	};
}
