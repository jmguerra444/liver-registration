/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/GUI/AlgorithmController.h>

#include <QtWidgets/QWidget>

class Ui_MRISegmentationController;
namespace ImFusion
{
	class MRISegmentationAlgorithm;

	/// MRISegmentationnstration of implementing a custom controller using Qt widgets.
	class MRISegmentationController
		: public QWidget
		, public AlgorithmController
	{
		Q_OBJECT

	public:
		/// Constructor with the algorithm instance
		MRISegmentationController(MRISegmentationAlgorithm* algorithm);

		/// Destructor
		virtual ~MRISegmentationController();

		/// Initializes the widget
		void init();

	public slots:
		/// Apply the chosen processing
		void onApply();

	protected:
		Ui_MRISegmentationController* m_ui;    ///< The actual GUI
		MRISegmentationAlgorithm* m_alg;       ///< The algorithm instance
	};
}
