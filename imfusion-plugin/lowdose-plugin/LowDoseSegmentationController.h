/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/GUI/AlgorithmController.h>

#include <QtWidgets/QWidget>

class Ui_LowDoseSegmentationController;
namespace ImFusion
{
	class LowDoseSegmentationAlgorithm;

	/// LowDoseSegmentationnstration of implementing a custom controller using Qt widgets.
	class LowDoseSegmentationController
		: public QWidget
		, public AlgorithmController
	{
		Q_OBJECT

	public:
		/// Constructor with the algorithm instance
		LowDoseSegmentationController(LowDoseSegmentationAlgorithm* algorithm);

		/// Destructor
		virtual ~LowDoseSegmentationController();

		/// Initializes the widget
		void init();

	public slots:
		/// Apply the chosen processing
		void onApply();

	protected:
		Ui_LowDoseSegmentationController* m_ui;    ///< The actual GUI
		LowDoseSegmentationAlgorithm* m_alg;       ///< The algorithm instance
	};
}
