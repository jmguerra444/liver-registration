#include "RegistrationController.h"

#include "RegistrationAlgorithm.h"

#include <ImFusion/Base/DataModel.h>
#include <ImFusion/Base/SharedImageSet.h>
#include <ImFusion/GUI/MainWindowBase.h>

#include "ui_RegistrationController.h"


namespace ImFusion
{
	RegistrationController::RegistrationController(RegistrationAlgorithm* algorithm)
		: AlgorithmController(algorithm)
		, m_alg(algorithm)
	{
		m_ui = new Ui_RegistrationController();
		m_ui->setupUi(this);
		connect(m_ui->pushButtonApply, SIGNAL(clicked()), this, SLOT(onApply()));
	}
	
	RegistrationController::~RegistrationController() { delete m_ui; }

	void RegistrationController::init() { addToAlgorithmDock(); }

	void RegistrationController::onApply()
	{
		m_alg->setDisplay(m_main->display());
		m_alg->setFactor(m_ui->spinBoxFactor->value());
		m_alg->compute();
		DataList d;
		m_alg->output(d);
		for (auto i : d.getImages(Data::UNKNOWN))
			m_main->dataModel()->add(i);
	}
}
