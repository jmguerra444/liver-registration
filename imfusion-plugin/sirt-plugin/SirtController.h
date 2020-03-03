/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/GUI/AlgorithmController.h>

#include <QtWidgets/QWidget>

class Ui_SirtController;
namespace ImFusion
{
	class SirtAlgorithm;

	/// Sirtnstration of implementing a custom controller using Qt widgets.
	class SirtController
		: public QWidget
		, public AlgorithmController
	{
		Q_OBJECT

	public:
		/// Constructor with the algorithm instance
		SirtController(SirtAlgorithm* algorithm);

		/// Destructor
		virtual ~SirtController();

		/// Initializes the widget
		void init();

	public slots:
		/// Apply the chosen processing
		void onApply();

	protected:
		Ui_SirtController* m_ui;    ///< The actual GUI
		SirtAlgorithm* m_alg;       ///< The algorithm instance
	};
}
