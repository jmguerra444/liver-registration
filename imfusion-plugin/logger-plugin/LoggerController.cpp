#include "LoggerController.h"
#include "LoggerAlgorithm.h"

#include "ImFusion/Base/Log.h"
#include <ImFusion/Base/DataModel.h>
#include <ImFusion/Base/SharedImageSet.h>
#include <ImFusion/GUI/MainWindowBase.h>

#include "ui_LoggerController.h"


namespace ImFusion
{
	LoggerController::LoggerController(LoggerAlgorithm* algorithm)
		: AlgorithmController(algorithm)
		, m_alg(algorithm)
	{
		m_ui = new Ui_LoggerController();
		m_ui->setupUi(this);
		connect(m_ui->pushButtonApply, SIGNAL(clicked()), this, SLOT(onApply()));
		connect(m_ui->pushButton, &QPushButton::clicked, [this]()
		{
			LOG_INFO("[SIRT][LOGGER] " << m_ui->lineEdit->text().toStdString());
		});
	}


	LoggerController::~LoggerController() { delete m_ui; }


	void LoggerController::init() { addToAlgorithmDock(); }


	void LoggerController::onApply()
	{
		m_alg->setFactor(m_ui->lineEdit->text().toStdString());
		m_alg->compute();
		DataList d;
		m_alg->output(d);
		for (auto i : d.getImages(Data::UNKNOWN))
			m_main->dataModel()->add(i);
	}
}
