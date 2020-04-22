#include "MRISegmentationAlgorithm.h"

#include <ImFusion/Base/DataList.h>
#include <ImFusion/Base/MemImage.h>
#include <ImFusion/Base/SharedImage.h>
#include <ImFusion/Base/SharedImageSet.h>
#include <ImFusion/Base/Log.h>
#include <ImFusion/Base/Properties.h>
#include <ImFusion/Base/Settings.h>
#include <ImFusion/ML/PixelwiseLearningAlgorithm.h>
#include <ImFusion/Base/ExtractImagesFromVolumeAlgorithm.h>
#include <ImFusion/Base/SplitChannelsAlgorithm.h>
#include <ImFusion/Base/CombineImagesAsVolumeAlgorithm.h>
#include <ImFusion/Base/DataList.h>

#include "QString"
#include "QDir"
#include "QCoreApplication"
#include "QFile"

#include <iostream>
#include <filesystem>

namespace ImFusion
{
	MRISegmentationAlgorithm::MRISegmentationAlgorithm(SharedImageSet* img)
		: m_imgIn(img)
	{
		LOG_INFO("Instance created");
	}


	bool MRISegmentationAlgorithm::createCompatible(const DataList& data, Algorithm** a)
	{
		// Check modality maybe
		
		// check requirements to create the algorithm
		if (data.size() != 1)
			return false;
		SharedImageSet* img = data.getImage(Data::UNKNOWN);    // in our case, any image is fine
		if (img == nullptr)
			return false;

		// requirements are met, create the algorithm if asked
		if (a)
		{
			*a = new MRISegmentationAlgorithm(img);
			(*a)->setInput(data);
		}
		return true;
	}


	void MRISegmentationAlgorithm::compute()
	{
		// set generic error status until we have finished
		m_status = static_cast<int>(Status::Error);

		m_imgOut = std::make_unique<SharedImageSet>();

		QString mriConfigurationFile = QCoreApplication::applicationDirPath() + "//plugins//SIRT//mri-liver.configtxt";

		DataList result_1; //DataOut
		PixelwiseLearningAlgorithm predictingAlgorithm(m_imgIn);
		predictingAlgorithm.setModelConfigPath(mriConfigurationFile.toStdString());
		predictingAlgorithm.compute();
		predictingAlgorithm.output(result_1);

		if (predictingAlgorithm.status() != 0) // Success
		{
			LOG_ERROR("Could not generate prediction");
			return;
		}

		auto predictionMultiChannel = std::make_unique<SharedImageSet*>(result_1.getImage());

		DataList result_2;
		SplitChannelsAlgorithm splitChannelsAlgorithm(*predictionMultiChannel);
		splitChannelsAlgorithm.setOutputSorting(SplitChannelsAlgorithm::GroupByFrame);
		splitChannelsAlgorithm.compute();
		splitChannelsAlgorithm.output(result_2);

		if (predictingAlgorithm.status() != 0)
		{
			LOG_ERROR("Split channels failed");
			return;
		}

		
		auto v = std::make_unique<SharedImage*>(result_2.getImage()->get());
		m_imgOut->add(*v.get());

		//auto b = std::make_unique<SharedImage*>(result_1.getImage()->get());
		//m_imgOut->add(*b.get());
		
		// set algorithm status to success
		m_status = static_cast<int>(Status::Success);
	}

	void MRISegmentationAlgorithm::output(DataList& dataOut)
	{
		// if we have produced some output, add it to the list
		// attention: membership is hereby transferred to the one calling output()
		if (m_imgOut)
			dataOut.add(m_imgOut.release());
	}


	void MRISegmentationAlgorithm::configure(const Properties* p)
	{
		// this method restores our members when a workspace file is loaded
		if (p == nullptr)
			return;

		p->param("thickness", m_thickness);
		for (int i = 0; i < (int)m_listeners.size(); ++i)
			m_listeners[i]->algorithmParametersChanged();
	}


	void MRISegmentationAlgorithm::configuration(Properties* p) const
	{
		// this method is necessary to store our settings in a workspace file
		if (p == nullptr)
			return;

		p->setParam("thickness", m_thickness, 2);
	}
}
