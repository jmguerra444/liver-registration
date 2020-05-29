/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/Base/Algorithm.h>
#include <ImFusion/Base/AlgorithmListener.h>

#include <memory>

namespace ImFusion
{
	class SharedImageSet;

	/// Simple LowDoseSegmentationnstration of a custom Algorithm.
	class LowDoseSegmentationAlgorithm : public Algorithm
	{
	public:
		/// Creates the algorithm instance with an image
		LowDoseSegmentationAlgorithm(SharedImageSet* img);

		/// Factory method to check for applicability or to create the algorithm
		static bool createCompatible(const DataList& data, Algorithm** a = 0);

		/// Applies the processing
		void compute() override;

		/// If new data was created, make it available here
		void output(DataList& dataOut) override;

		/// \name	Methods implementing the Configurable interface
		void configure(const Properties* p) override;
		void configuration(Properties* p) const override;


		// Used algorithms
		SharedImageSet* doDilatation(SharedImageSet* sis, int size);
		SharedImageSet* doErosion(SharedImageSet* sis, int size);
		double volumeFromLabelMap(SharedImageSet* sis);

	private:
		SharedImageSet* m_imgIn = nullptr;           /// Lowdose volume
		std::unique_ptr<SharedImageSet> m_imgOut;    ///< Output image after processing
	};
}
