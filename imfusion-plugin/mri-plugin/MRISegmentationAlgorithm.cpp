#include "MRISegmentationAlgorithm.h"

#include <ImFusion/Base/DataList.h>
#include <ImFusion/Base/MemImage.h>
#include <ImFusion/Base/Log.h>
#include <ImFusion/Base/Properties.h>
#include <ImFusion/Base/Settings.h>
#include <ImFusion/Base/ExtractImagesFromVolumeAlgorithm.h>
#include <ImFusion/Base/SplitChannelsAlgorithm.h>
#include <ImFusion/Base/MeshProcessing.h>
#include <ImFusion/Seg/LabelToMeshAlgorithm.h>
#include <ImFusion/ML/PixelwiseLearningAlgorithm.h>
#include <ImFusion/Base/Mesh.h>

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

		// DO PREDICTION
		DataList result1; //DataOut
		PixelwiseLearningAlgorithm predictingAlgorithm(m_imgIn);
		predictingAlgorithm.setModelConfigPath(mriConfigurationFile.toStdString());
		predictingAlgorithm.compute();
		predictingAlgorithm.output(result1);
		if (predictingAlgorithm.status() != 0) // Success
		{
			LOG_ERROR("Could not generate prediction");
			return;
		}

		// SPLIT CHANNELS
		auto result1SIS = std::make_unique<SharedImageSet>(*result1.getImage());
		DataList result_2;
		SplitChannelsAlgorithm splitChannelsAlgorithm(result1SIS.get());
		splitChannelsAlgorithm.setOutputSorting(SplitChannelsAlgorithm::GroupByChannel);
		splitChannelsAlgorithm.compute();
		splitChannelsAlgorithm.output(result_2);
		if (predictingAlgorithm.status() != 0)
		{
			LOG_ERROR("Split channels failed");
			return;
		}

		auto b = std::make_unique<SharedImageSet>(*result_2.getImage());
		DataList result_3;
		LabelToMeshAlgorithm labelToMeshAlgorithm(b.get());
		labelToMeshAlgorithm.setIsoValue(0.5);
		labelToMeshAlgorithm.setAboveIsoValue(true);
		labelToMeshAlgorithm.setSmoothing(0);
		labelToMeshAlgorithm.compute();
		labelToMeshAlgorithm.output(result_3);

		//
		auto y = result_3.getSurfaces();
		LOG_ERROR(y[0]->numberOfVertices() << "   " << y[0]->numberOfFaces());
		
		LOG_ERROR("V" << MeshProcessing::computeVolume(y[0]));
		LOG_ERROR("1" << y[0]->isValid());
		LOG_ERROR("2" << y[0]->origin());
		LOG_ERROR("3" << y[0]->center());
		LOG_ERROR("4" << y[0]->listHoles().size());


		
		// ADD TO DisplayWidgetMulti
		m_imgOut->add(b->get());
		m_status = static_cast<int>(Status::Success);
	}

	void MRISegmentationAlgorithm::output(DataList& dataOut)
	{
		// if we have produced some output, add it to the list
		// attention: membership is hereby transferred to the one calling output()
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
