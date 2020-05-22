/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/Base/Algorithm.h>
#include <ImFusion/Base/AlgorithmListener.h>

#include <memory>

namespace ImFusion
{
	class SharedImageSet;

	/// Simple Loggernstration of a custom Algorithm.
	/// This algorithm will downsample the input image by the specified factor.
	class LoggerAlgorithm : public Algorithm
	{
	public:
		/// Creates the algorithm instance with an image
		LoggerAlgorithm(SharedImageSet* img);

		/// Set downsampling factor
		void setFactor(std::string msg) { m_message = msg; }

		/// \name	Methods implementing the algorithm interface
		//\{
		/// Factory method to check for applicability or to create the algorithm
		static bool createCompatible(const DataList& data, Algorithm** a = 0);

		/// Applies the processing
		void compute() override;

		/// If new data was created, make it available here
		void output(DataList& dataOut) override;
		//\}

		/// \name	Methods implementing the Configurable interface
		//\{
		void configure(const Properties* p) override;
		void configuration(Properties* p) const override;
		//\}

	private:
		SharedImageSet* m_imgIn = nullptr;           ///< Input image to process
		std::unique_ptr<SharedImageSet> m_imgOut;    ///< Output image after processing
		std::string m_message = "";                            ///< Downsampling factor
	};
}
