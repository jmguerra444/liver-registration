#include "LinkPoseAlgorithm.h"

#include <ImFusion/GUI/DisplayWidgetMulti.h>
#include <ImFusion/GUI/ImageView2D.h>
#include <ImFusion/GUI/ImageView3D.h>
#include <ImFusion/GL/GlSlice.h>

#include <ImFusion/Base/DataList.h>
#include <ImFusion/Base/MemImage.h>
#include <ImFusion/Base/SharedImage.h>
#include <ImFusion/Base/SharedImageSet.h>
#include <ImFusion/Base/BasicImageProcessing.h>
#include <ImFusion/Base/Data.h>
#include <ImFusion/Reg/ImageRegistration.h>

// Optimizers
#include <ImFusion/Base/OptimizerNL.h>


namespace ImFusion
{
	LinkPoseAlgorithm::LinkPoseAlgorithm(SharedImageSet* vol, SharedImageSet* mask)
		: m_volume_1(vol)
		, m_volume_2(mask)
	{
		
	}
	
	bool LinkPoseAlgorithm::createCompatible(const DataList& data, Algorithm** a)
	{
		// check requirements to create the algorithm
		if (data.size() != 2)
			return false;

		SharedImageSet* volume_1 = data.getImages()[0];
		SharedImageSet* volume_2 = data.getImages()[1];


		if (volume_1 == nullptr || volume_2==nullptr)
			return false;

		// requirements are met, create the algorithm if asked
		if (a)
		{
			*a = new LinkPoseAlgorithm(volume_1, volume_2);
			(*a)->setInput(data);
		}
		return true;
	}


	void LinkPoseAlgorithm::compute()
	{
		m_status = static_cast<int>(Status::Error);
		m_imgOut = std::make_unique<SharedImageSet>();
		setDisplay();

		m_volume_2->setDeformation(m_volume_1->deformation());
		// set algorithm status to success
		m_status = static_cast<int>(Status::Success);
	}


	void LinkPoseAlgorithm::output(DataList& dataOut)
	{
		// if we have produced some output, add it to the list
		// attention: membership is hereby transferred to the one calling output()
		//if (m_imgOut)
		//	dataOut.add(m_imgOut.release());
	}


	void LinkPoseAlgorithm::configure(const Properties* p)
	{
		// this method restores our members when a workspace file is loaded
		if (p == nullptr)
			return;
		for (int i = 0; i < (int)m_listeners.size(); ++i)
			m_listeners[i]->algorithmParametersChanged();
	}


	void LinkPoseAlgorithm::configuration(Properties* p) const
	{
		// this method is necessary to store our settings in a workspace file
		if (p == nullptr)
			return;
	}

	void LinkPoseAlgorithm::setDisplay()
	{
		if (m_display == nullptr)
			return;

		// DO STUFF HERE, ADJUST BLENDING ETC ETC. :-)
	}
}