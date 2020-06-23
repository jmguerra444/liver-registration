#include "LinkPoseController.h"

#include "LinkPoseAlgorithm.h"

#include <ImFusion/Base/DataModel.h>
#include <ImFusion/Base/SharedImageSet.h>
#include <ImFusion/GUI/MainWindowBase.h>

#include "ui_LinkPoseController.h"


namespace ImFusion
{
	LinkPoseController::LinkPoseController(LinkPoseAlgorithm* algorithm)
		: AlgorithmController(algorithm)
		, m_alg(algorithm)
	{
		m_ui = new Ui_LinkPoseController();
		m_ui->setupUi(this);
		connect(m_ui->pushButtonApply, SIGNAL(clicked()), this, SLOT(onApply()));
	}
	
	LinkPoseController::~LinkPoseController() { delete m_ui; }

	void LinkPoseController::init() { addToAlgorithmDock(); }

	void LinkPoseController::onApply()
	{
		m_alg->setDisplay(m_main->display());
		m_alg->compute();
		DataList d;
		m_alg->output(d);
		for (auto i : d.getImages(Data::UNKNOWN))
			m_main->dataModel()->add(i);
	}
}
