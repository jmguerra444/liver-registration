/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/GUI/AlgorithmController.h>

#include <QtWidgets/QWidget>

class Ui_LinkPoseController;
namespace ImFusion
{
	class LinkPoseAlgorithm;

	/// LinkPosenstration of implementing a custom controller using Qt widgets.
	class LinkPoseController
		: public QWidget
		, public AlgorithmController
	{
		Q_OBJECT

	public:
		/// Constructor with the algorithm instance
		LinkPoseController(LinkPoseAlgorithm* algorithm);

		/// Destructor
		virtual ~LinkPoseController();

		/// Initializes the widget
		void init();

	public slots:
		/// Apply the chosen processing
		void onApply();

	protected:
		Ui_LinkPoseController* m_ui;    ///< The actual GUI
		LinkPoseAlgorithm* m_alg;       ///< The algorithm instance
	};
}
