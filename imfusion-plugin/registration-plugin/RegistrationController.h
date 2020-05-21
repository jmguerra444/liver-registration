/* Copyright (c) 2012-2019 ImFusion GmbH, Munich, Germany. All rights reserved. */
#pragma once

#include <ImFusion/GUI/AlgorithmController.h>

#include <QtWidgets/QWidget>

class Ui_RegistrationController;
namespace ImFusion
{
	class RegistrationAlgorithm;

	/// Registrationnstration of implementing a custom controller using Qt widgets.
	class RegistrationController
		: public QWidget
		, public AlgorithmController
	{
		Q_OBJECT

	public:
		/// Constructor with the algorithm instance
		RegistrationController(RegistrationAlgorithm* algorithm);

		/// Destructor
		virtual ~RegistrationController();

		/// Initializes the widget
		void init();

	public slots:
		/// Apply the chosen processing
		void onApply();

	protected:
		Ui_RegistrationController* m_ui;    ///< The actual GUI
		RegistrationAlgorithm* m_alg;       ///< The algorithm instance
	};
}
