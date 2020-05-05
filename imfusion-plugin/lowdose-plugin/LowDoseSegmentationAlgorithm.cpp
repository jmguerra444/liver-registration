#include "LowDoseSegmentationAlgorithm.h"

#include <ImFusion/Base/DataList.h>
#include <ImFusion/Base/MemImage.h>
#include <ImFusion/Base/Log.h>
#include <ImFusion/Base/Properties.h>
#include <ImFusion/Base/Settings.h>
#include <ImFusion/Base/ExtractImagesFromVolumeAlgorithm.h>
#include <ImFusion/Base/CombineImagesAsVolumeAlgorithm.h>
#include <ImFusion/Base/SplitChannelsAlgorithm.h>
#include <ImFusion/Base/Mesh.h>
#include <ImFusion/Seg/LabelToMeshAlgorithm.h>
#include <ImFusion/ML/PixelwiseLearningAlgorithm.h>

#include "QString"
#include "QDir"
#include "QCoreApplication"
#include "QFile"

#include <iostream>
#include <filesystem>

namespace ImFusion
{
	LowDoseSegmentationAlgorithm::LowDoseSegmentationAlgorithm(SharedImageSet* img)
		: m_imgIn(img)
	{
		LOG_INFO("Instance created");
	}


	bool LowDoseSegmentationAlgorithm::createCompatible(const DataList& data, Algorithm** a)
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
			*a = new LowDoseSegmentationAlgorithm(img);
			(*a)->setInput(data);
		}
		return true;
	}


	void LowDoseSegmentationAlgorithm::compute()
	{
		// set generic error status until we have finished
		m_status = static_cast<int>(Status::Error);

		m_imgOut = std::make_unique<SharedImageSet>();
		QString lowdoseConfigurationFile = QCoreApplication::applicationDirPath() + "//plugins//SIRT//lowdose-liver.configtxt";
	
		// EXTRACT IMAGES FROM VOLUME
		DataList images;
		ImFusion::ExtractImagesFromVolumeAlgorithm imageExtractor(m_imgIn);
		imageExtractor.compute();
		imageExtractor.output(images);
		auto sis = std::make_unique<SharedImageSet>(images.getImage());

		// PREDICT
		DataList result_1;
		PixelwiseLearningAlgorithm predictingAlgorithm(sis.get());
		predictingAlgorithm.setModelConfigPath(lowdoseConfigurationFile.toStdString());
		predictingAlgorithm.setInput(images);
		predictingAlgorithm.compute();
		predictingAlgorithm.output(result_1);
		if(predictingAlgorithm.status() != 0) // Success
		{
			LOG_ERROR("Could not generate prediction");
			return;
		}

		// TODO: Make it detect thickness automatic
		auto properties = std::make_unique<Properties>();
		properties->setParam("Slice Thickness", m_thickness);
		LOG_INFO(m_thickness);

		auto result1SIS = std::make_unique<std::vector<SharedImage*>>(result_1.getImage()->images());
		DataList result_2;
		CombineImagesAsVolumeAlgorithm convertToVolumeAlgorithm(*result1SIS.get());
		convertToVolumeAlgorithm.configure(properties.get());
		convertToVolumeAlgorithm.compute();
		convertToVolumeAlgorithm.output(result_2);
		if(convertToVolumeAlgorithm.status() != 0)
		{
			LOG_ERROR("Could not convert to volume");
			return;
		}

		// SPLIT CHANNELS
		auto result2SIS = std::make_unique<SharedImageSet>(*result_2.getImage());
		DataList result_3;
		SplitChannelsAlgorithm splitChannelsAlgorithm(result2SIS.get());
		splitChannelsAlgorithm.setOutputSorting(SplitChannelsAlgorithm::GroupByFrame);
		splitChannelsAlgorithm.compute();
		splitChannelsAlgorithm.output(result_2);
		if (predictingAlgorithm.status() != 0)
		{
			LOG_ERROR("Split channels failed");
			return;
		}

		// GENERATE MESH TO COMPUTE VOLUME
		auto result2SIS = std::make_unique<SharedImageSet>(*result_2.getImage());
		DataList result_3;
		LabelToMeshAlgorithm labelToMeshAlgorithm(result2SIS.get());
		labelToMeshAlgorithm.setIsoValue(0.5);
		labelToMeshAlgorithm.setAboveIsoValue(true);
		labelToMeshAlgorithm.setSmoothing(0);
		labelToMeshAlgorithm.compute();
		labelToMeshAlgorithm.output(result_3);
		if (labelToMeshAlgorithm.status() != 0)
		{
			LOG_ERROR("Can't extract meshes");
			return;
		}

		auto v = std::make_unique<SharedImage*>(result_2.getImage()->get());
		m_imgOut->add(*v.get());
		
		// set algorithm status to success
		m_status = static_cast<int>(Status::Success);
	}

	void LowDoseSegmentationAlgorithm::output(DataList& dataOut)
	{
		// if we have produced some output, add it to the list
		// attention: membership is hereby transferred to the one calling output()
		if (m_imgOut)
			dataOut.add(m_imgOut.release());
	}


	void LowDoseSegmentationAlgorithm::configure(const Properties* p)
	{
		// this method restores our members when a workspace file is loaded
		if (p == nullptr)
			return;

		p->param("thickness", m_thickness);
		for (int i = 0; i < (int)m_listeners.size(); ++i)
			m_listeners[i]->algorithmParametersChanged();
	}


	void LowDoseSegmentationAlgorithm::configuration(Properties* p) const
	{
		// this method is necessary to store our settings in a workspace file
		if (p == nullptr)
			return;

		p->setParam("thickness", m_thickness, 2);
	}
}
