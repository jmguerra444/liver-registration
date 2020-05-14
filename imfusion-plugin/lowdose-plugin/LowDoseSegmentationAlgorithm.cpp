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
#include <ImFusion/Base/MeshPostProcessingAlgorithm.h>
#include <ImFusion/Base/MeshProcessing.h>
#include <ImFusion/Base/LinkPose.h>
#include <ImFusion/Base/MeshToLabelMapAlgorithm.h>
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

		if (m_imgIn->modality() == Data::CT)
		{
			LOG_INFO("[SIRT] CT volume correctly detected");
		}else
		{
			LOG_ERROR("[SIRT] Not a CT volume");
			return;
		}
		
		auto thickness = m_imgIn->mem()->spacing().z();
		LOG_INFO("[SIRT] Slice thickness:  " << thickness << " mm");

		QString lowdoseConfigurationFile = QCoreApplication::applicationDirPath() + "//plugins//SIRT//lowdose-liver.configtxt";
	
		// EXTRACT IMAGES FROM VOLUME
		DataList images;
		ImFusion::ExtractImagesFromVolumeAlgorithm imageExtractor(m_imgIn);
		imageExtractor.compute();
		imageExtractor.output(images);
		auto sis = std::make_unique<SharedImageSet>(images.getImage());

		// PREDICT
		DataList result_1;
		{
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
		}

		// TODO: Make it detect thickness automatic
		auto properties = std::make_unique<Properties>();
		properties->setParam("Slice Thickness", thickness);

		auto p = std::make_unique<std::vector<SharedImage*>>(result_1.getImage()->images());
		DataList result_2;
		{
			CombineImagesAsVolumeAlgorithm convertToVolumeAlgorithm(*p);
			convertToVolumeAlgorithm.configure(properties.get());
			convertToVolumeAlgorithm.compute();
			convertToVolumeAlgorithm.output(result_2);
			if(convertToVolumeAlgorithm.status() != 0)
			{
				LOG_ERROR("Could not convert to volume");
				return;
			}
		}

		// SPLIT CHANNELS
		auto result2SIS = std::make_unique<SharedImageSet>(*result_2.getImage());
		DataList result_3;
		{
			SplitChannelsAlgorithm splitChannelsAlgorithm(result2SIS.get());
			splitChannelsAlgorithm.setOutputSorting(SplitChannelsAlgorithm::GroupByFrame);
			splitChannelsAlgorithm.compute();
			splitChannelsAlgorithm.output(result_3);
			if (splitChannelsAlgorithm.status() != 0)
			{
				LOG_ERROR("Split channels failed");
				return;
			}
		}

		// GENERATE MESH TO COMPUTE VOLUME
		auto result3SIS = std::make_unique<SharedImageSet>(*result_3.getImage());
		DataList result_4;
		{
			LabelToMeshAlgorithm labelToMeshAlgorithm(result3SIS.get());
			labelToMeshAlgorithm.setIsoValue(0.5);
			labelToMeshAlgorithm.setAboveIsoValue(true);
			labelToMeshAlgorithm.setSmoothing(0);
			labelToMeshAlgorithm.compute();
			labelToMeshAlgorithm.output(result_4);
			if (labelToMeshAlgorithm.status() != 0)
			{
				LOG_ERROR("Can't extract meshes");
				return;
			}
		}

		//// DO SOME MESH POST PROCESSING
		auto mesh = result_4.getSurfaces()[0];
		MeshPostProcessingAlgorithm meshPostProcessingAlgorithm(mesh);
		meshPostProcessingAlgorithm.setMode(MeshPostProcessingAlgorithm::Mode::FILL_HOLES);
		meshPostProcessingAlgorithm.compute();
		MeshProcessing::reduceToOneComponent(mesh);
		if (meshPostProcessingAlgorithm.status() != 0)
		{
			LOG_ERROR("Can't do post-processing");
			return;
		}
		LOG_INFO("[SIRT] Volume:  " << MeshProcessing::computeVolume(mesh) / 1e3 << " ml");

		DataList result_5;
		{
			MeshToLabelMapAlgorithm meshToLabelMapAlgorithm(mesh, m_imgIn);
			auto meshToLabelMapProperties = std::make_unique<Properties>();
			meshToLabelMapProperties->setParam("Output Spacing", 1);
			meshToLabelMapProperties->setParam("Margin", 10);
			meshToLabelMapProperties->setParam("InsideValue", 1);
			meshToLabelMapProperties->setParam("Outside Value", 0);
			meshToLabelMapAlgorithm.configure(meshToLabelMapProperties.get());
			meshToLabelMapAlgorithm.compute();
			meshToLabelMapAlgorithm.output(result_5);
			if (meshToLabelMapAlgorithm.status() != 0)
			{
				LOG_ERROR("Can't create label map");
				return;
			}
		}
		auto result5SIS = std::make_unique<SharedImageSet>(*result_5.getImage());

		
		// MANAGE SOME RESOURCES
		result_2.clear();
		result_3.clear();
		
		 //set algorithm status to success
		m_imgOut->add(result5SIS->get());
		m_status = static_cast<int>(Status::Success);
	}

	void LowDoseSegmentationAlgorithm::output(DataList& dataOut)
	{
		// if we have produced some output, add it to the list
		// attention: membership is hereby transferred to the one calling output()

		auto linkedPose = new LinkPose(DataList{ m_imgOut.get(), m_imgIn });

		if (m_imgOut)
			dataOut.add(m_imgOut.release());
	}


	void LowDoseSegmentationAlgorithm::configure(const Properties* p)
	{
		// this method restores our members when a workspace file is loaded
		if (p == nullptr)
			return;

		for (int i = 0; i < (int)m_listeners.size(); ++i)
			m_listeners[i]->algorithmParametersChanged();
	}


	void LowDoseSegmentationAlgorithm::configuration(Properties* p) const
	{
		// this method is necessary to store our settings in a workspace file
		if (p == nullptr)
			return;
	}
}
