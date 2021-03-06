#include "MRISegmentationAlgorithm.h"

#include <ImFusion/Base/DataList.h>
#include <ImFusion/Base/MemImage.h>
#include <ImFusion/Base/Log.h>
#include <ImFusion/Base/Properties.h>
#include <ImFusion/Base/Settings.h>
#include <ImFusion/Base/ExtractImagesFromVolumeAlgorithm.h>
#include <ImFusion/Base/SplitChannelsAlgorithm.h>
#include <ImFusion/Base/MeshProcessing.h>
#include <ImFusion/Base/MeshPostProcessingAlgorithm.h>
#include <ImFusion/Base/MeshToLabelMapAlgorithm.h>
#include <ImFusion/Base/LinkPose.h>
#include <ImFusion/Base/Mesh.h>
#include <ImFusion/Seg/LabelToMeshAlgorithm.h>
#include <ImFusion/ML/PixelwiseLearningAlgorithm.h>

#include "QString"
#include "QDir"
#include "QCoreApplication"
#include "QFile"
#include "QDateTime"

#include <iostream>
#include <filesystem>
#include <fstream>

namespace ImFusion
{
	MRISegmentationAlgorithm::MRISegmentationAlgorithm(SharedImageSet* img)
		: m_imgIn(img)
	{
		LOG_INFO("[SIRT] Instance created");
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

		if (m_imgIn->modality() == Data::MRI)
		{
			LOG_INFO("[SIRT] MRI volume correctly detected");
		}
		else
		{
			LOG_ERROR("[SIRT] Not a MRI volume");
			return;
		}

		QString mriConfigurationFile = QCoreApplication::applicationDirPath() + "//plugins//SIRT//mri-liver.configtxt";

		// DO PREDICTION
		DataList result_1; //DataOut
		{
			PixelwiseLearningAlgorithm predictingAlgorithm(m_imgIn);
			predictingAlgorithm.setModelConfigPath(mriConfigurationFile.toStdString());
			predictingAlgorithm.compute();
			predictingAlgorithm.output(result_1);
			if (predictingAlgorithm.status() != 0) // Success
			{
				LOG_ERROR("Could not generate prediction");
				return;
			}
		}
		// SPLIT CHANNELS
		auto result1SIS = std::make_unique<SharedImageSet>(*result_1.getImage());
		DataList result_2;
		{
			SplitChannelsAlgorithm splitChannelsAlgorithm(result1SIS.get());
			splitChannelsAlgorithm.setOutputSorting(SplitChannelsAlgorithm::GroupByChannel);
			splitChannelsAlgorithm.compute();
			splitChannelsAlgorithm.output(result_2);
			if (splitChannelsAlgorithm.status() != 0)
			{
				LOG_ERROR("Split channels failed");
				return;
			}
		}

		// GENERATE MESH TO COMPUTE VOLUME
		auto result2SIS = std::make_unique<SharedImageSet>(*result_2.getImage());
		DataList result_3;
		{
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
		}

		// POST PROCESSING ALGORITHM
		auto mesh = result_3.getSurfaces()[0];
		MeshPostProcessingAlgorithm meshPostProcessingAlgorithm(mesh);
		meshPostProcessingAlgorithm.setMode(MeshPostProcessingAlgorithm::Mode::FILL_HOLES);
		meshPostProcessingAlgorithm.compute();
		MeshProcessing::reduceToOneComponent(mesh);
		if (meshPostProcessingAlgorithm.status() != 0)
		{
			LOG_ERROR("Can't do post-processing");
			return;
		}
		auto v = MeshProcessing::computeVolume(mesh) / 1e3;
		LOG_INFO("[SIRT] Volume:  " << v << " ml");

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

		// SAVE OUR RESULTS
		std::string filename = "C:\\Master thesis\\master\\kri-evaluation\\plugin-volumetry-mri.txt";
		std::ofstream outfile;
		outfile.open(filename, std::ios_base::app);
		outfile << "[SIRT] " << QDateTime::currentDateTime().toString("dd.MM.yyyy hh:mm").toStdString() << "  " << v << std::endl;
		outfile.close();
		
		m_imgOut->add(result5SIS->get());
		m_status = static_cast<int>(Status::Success);
	}

	void MRISegmentationAlgorithm::output(DataList& dataOut)
	{
		// if we have produced some output, add it to the list
		// attention: membership is hereby transferred to the one calling output()

		m_imgOut->setName("MRI Mask");
		//// LINK POSE
		auto linkedPose = new LinkPose(DataList{ m_imgOut.get(), m_imgIn });

		if (m_imgOut)
		{
			dataOut.add(m_imgOut.release());
		}
	}


	void MRISegmentationAlgorithm::configure(const Properties* p)
	{
		// this method restores our members when a workspace file is loaded
		if (p == nullptr)
			return;

		for (int i = 0; i < (int)m_listeners.size(); ++i)
			m_listeners[i]->algorithmParametersChanged();
	}


	void MRISegmentationAlgorithm::configuration(Properties* p) const
	{
		// this method is necessary to store our settings in a workspace file
		if (p == nullptr)
			return;
	}
}
