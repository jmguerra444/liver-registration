#include "LowDoseSegmentationController.h"

#include "LowDoseSegmentationAlgorithm.h"

#include <ImFusion/Base/DataModel.h>
#include <ImFusion/Base/SharedImageSet.h>
#include <ImFusion/GUI/MainWindowBase.h>

#include "ui_LowDoseSegmentationController.h"


namespace ImFusion
{
	LowDoseSegmentationController::LowDoseSegmentationController(LowDoseSegmentationAlgorithm* algorithm)
		: AlgorithmController(algorithm)
		, m_alg(algorithm)
	{
		m_ui = new Ui_LowDoseSegmentationController();
		m_ui->setupUi(this);
		connect(m_ui->pushButtonApply, SIGNAL(clicked()), this, SLOT(onApply()));
	}


	LowDoseSegmentationController::~LowDoseSegmentationController() { delete m_ui; }


	void LowDoseSegmentationController::init() { addToAlgorithmDock(); }


	void LowDoseSegmentationController::onApply()
	{
		m_alg->compute();
		DataList d;
		m_alg->output(d);
		for (auto i : d.getImages(Data::UNKNOWN))
			m_main->dataModel()->add(i);
	}
}
