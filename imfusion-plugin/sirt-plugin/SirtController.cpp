#include "SirtController.h"

#include "SirtAlgorithm.h"

#include <ImFusion/Base/DataModel.h>
#include <ImFusion/Base/SharedImageSet.h>
#include <ImFusion/GUI/MainWindowBase.h>

#include "ui_SirtController.h"


namespace ImFusion
{
	SirtController::SirtController(SirtAlgorithm* algorithm)
		: AlgorithmController(algorithm)
		, m_alg(algorithm)
	{
		m_ui = new Ui_SirtController();
		m_ui->setupUi(this);
		connect(m_ui->pushButtonApply, SIGNAL(clicked()), this, SLOT(onApply()));
	}


	SirtController::~SirtController() { delete m_ui; }


	void SirtController::init() { addToAlgorithmDock(); }


	void SirtController::onApply()
	{
		m_alg->setFactor(m_ui->spinBoxFactor->value());
		m_alg->compute();
		DataList d;
		m_alg->output(d);
		for (auto i : d.getImages(Data::UNKNOWN))
			m_main->dataModel()->add(i);
	}
}
