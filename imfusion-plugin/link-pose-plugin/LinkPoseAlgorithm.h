/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/Base/Algorithm.h>
#include <ImFusion/Base/AlgorithmListener.h>

#include <memory>

namespace ImFusion
{
	class SharedImageSet;
	class DisplayWidgetMulti;
	class Data;
	
	/// Simple LinkPosenstration of a custom Algorithm.
	/// This algorithm will downsample the input image by the specified factor.
	class LinkPoseAlgorithm : public Algorithm
	{
	public:
		/// Creates the algorithm instance with an image
		/// img1: reference, mask: moving
		LinkPoseAlgorithm(SharedImageSet* volume_1, SharedImageSet* volume_2);

		/// Set downsampling factor
		void setDisplay(DisplayWidgetMulti* disp){ m_display = disp; }
		void setDisplay();

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
		DisplayWidgetMulti* m_display = nullptr;
		SharedImageSet* m_volume_1 = nullptr;           ///mri mask
		SharedImageSet* m_volume_2 = nullptr;           ///lowdose mask
		std::unique_ptr<SharedImageSet> m_imgOut;    ///< Output image after processing
	};
}
