/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/GUI/AlgorithmController.h>

#include <QtWidgets/QWidget>

class Ui_LoggerController;
namespace ImFusion
{
	class LoggerAlgorithm;

	/// Loggernstration of implementing a custom controller using Qt widgets.
	class LoggerController
		: public QWidget
		, public AlgorithmController
	{
		Q_OBJECT

	public:
		/// Constructor with the algorithm instance
		LoggerController(LoggerAlgorithm* algorithm);

		/// Destructor
		virtual ~LoggerController();

		/// Initializes the widget
		void init();

	public slots:
		/// Apply the chosen processing
		void onApply();

	protected:
		Ui_LoggerController* m_ui;    ///< The actual GUI
		LoggerAlgorithm* m_alg;       ///< The algorithm instance
	};
}
