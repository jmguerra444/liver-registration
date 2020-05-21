#include "RegistrationAlgorithm.h"

#include <ImFusion/GUI/DisplayWidgetMulti.h>
#include <ImFusion/GUI/ImageView2D.h>
#include <ImFusion/GUI/ImageView3D.h>
#include <ImFusion/GL/GlSlice.h>

#include <ImFusion/Base/DataList.h>
#include <ImFusion/Base/MemImage.h>
#include <ImFusion/Base/SharedImage.h>
#include <ImFusion/Base/SharedImageSet.h>
#include <ImFusion/Base/BasicImageProcessing.h>
#include <ImFusion/Reg/ImageRegistration.h>

// Optimizers
#include <ImFusion/Base/OptimizerNL.h>


namespace ImFusion
{
	RegistrationAlgorithm::RegistrationAlgorithm(SharedImageSet* ref, SharedImageSet* mov)
		: m_reference(ref)
		, m_moving(mov)
	{
		
	}


	bool RegistrationAlgorithm::createCompatible(const DataList& data, Algorithm** a)
	{
		// check requirements to create the algorithm
		if (data.size() != 2)
			return false;
		
		SharedImageSet* mov = data.getImage(Data::UNKNOWN, Data::Modality::MRI);
		SharedImageSet* ref = data.getImage(Data::UNKNOWN, Data::Modality::CT);

		if (mov == nullptr || ref==nullptr)
			return false;

		// requirements are met, create the algorithm if asked
		if (a)
		{
			*a = new RegistrationAlgorithm(mov, ref);
			(*a)->setInput(data);
		}
		return true;
	}


	void RegistrationAlgorithm::compute()
	{
		// set generic error status until we have finished
		m_status = static_cast<int>(Status::Error);
		m_imgOut = std::make_unique<SharedImageSet>();
		setDisplay();

		LOG_ERROR(m_moving->describe());
		LOG_ERROR(m_reference->describe());
		
		//  REGISTRATION ONE
		const static double K_PARAMETER_TOLERANCE = 0.01;
		const static double K_PARAMETER_STEP_SIZE = 2.0;
		const static int K_OPTIMIZER_TYPE = 34; // BOBYQA
		const static int K_N_TRIES_FOR_RANDOM_STUDY = 20;
		const static double K_PARAMETER_RANGE = 80;

		//auto staticVolume = std::unique_ptr<ImFusion::SharedImageSet>(m_reference);
		//auto movingVolume = std::unique_ptr<ImFusion::SharedImageSet>(m_moving);

		//for (auto sis : { m_reference, m_moving })
		//{
		//	BasicImageProcessing bip(sis);
		//	bip.setCreateNew(false);
		//	bip.setMode(BasicImageProcessing::NORMALIZE);
		//	bip.compute();
		//}

		mat4 movingVolumeMatrix = m_moving->matrixToWorld();
		movingVolumeMatrix.block<3, 1>(0, 3) = m_reference->matrixToWorld().block<3, 1>(0, 3);
		m_moving->setMatrixToWorld(movingVolumeMatrix);

		//ImageRegistration registration(m_reference, m_moving);
		//auto opt = std::make_shared<ImFusion::OptimizerNL>(registration.optimizer()->dimension(), K_OPTIMIZER_TYPE);
		//opt->setAbortParTol(K_PARAMETER_TOLERANCE);
		//opt->setStep(K_PARAMETER_STEP_SIZE);
		//registration.setOptimizer(opt);
		//registration.computePreprocessing();
		//registration.compute();

		// set algorithm status to success
		m_status = static_cast<int>(Status::Success);
	}


	void RegistrationAlgorithm::output(DataList& dataOut)
	{
		// if we have produced some output, add it to the list
		// attention: membership is hereby transferred to the one calling output()
		if (m_imgOut)
			dataOut.add(m_imgOut.release());
	}


	void RegistrationAlgorithm::configure(const Properties* p)
	{
		// this method restores our members when a workspace file is loaded
		if (p == nullptr)
			return;

		p->param("factor", m_factor);
		for (int i = 0; i < (int)m_listeners.size(); ++i)
			m_listeners[i]->algorithmParametersChanged();
	}


	void RegistrationAlgorithm::configuration(Properties* p) const
	{
		// this method is necessary to store our settings in a workspace file
		if (p == nullptr)
			return;

		p->setParam("factor", m_factor, 2);
	}

	void RegistrationAlgorithm::setDisplay()
	{
		if (m_display == nullptr)
			return;

		// DO STUFF HERE, ADJUST BLENDING ETC ETC. :-)
	}
}