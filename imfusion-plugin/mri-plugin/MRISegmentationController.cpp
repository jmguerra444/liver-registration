#include "MRISegmentationController.h"

#include "MRISegmentationAlgorithm.h"

#include <ImFusion/Base/DataModel.h>
#include <ImFusion/Base/SharedImageSet.h>
#include <ImFusion/GUI/MainWindowBase.h>

#include "ui_MRISegmentationController.h"


namespace ImFusion
{
	MRISegmentationController::MRISegmentationController(MRISegmentationAlgorithm* algorithm)
		: AlgorithmController(algorithm)
		, m_alg(algorithm)
	{
		m_ui = new Ui_MRISegmentationController();
		m_ui->setupUi(this);
		connect(m_ui->pushButtonApply, SIGNAL(clicked()), this, SLOT(onApply()));
	}


	MRISegmentationController::~MRISegmentationController() { delete m_ui; }


	void MRISegmentationController::init() { addToAlgorithmDock(); }


	void MRISegmentationController::onApply()
	{
		m_alg->compute();
		DataList d;
		m_alg->output(d);
		for (auto i : d.getImages(Data::UNKNOWN))
			m_main->dataModel()->add(i);
	}
}
