/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/Base/AlgorithmControllerFactory.h>
#include <ImFusion/Base/AlgorithmFactory.h>

namespace ImFusion
{
	class Algorithm;

	/// AlgorithmFactory for LinkPose plugin
	class LinkPoseAlgorithmFactory : public AlgorithmFactory
	{
	public:
		LinkPoseAlgorithmFactory();
	};

	/// AlgorithmControllerFactory for LinkPose plugin
	class LinkPoseControllerFactory : public AlgorithmControllerFactory
	{
	public:
		virtual AlgorithmController* create(Algorithm* a) const;
	};
}
