#include "LoggerAlgorithm.h"

#include "ImFusion/Base/Log.h"

#include <ImFusion/Base/DataList.h>
#include <ImFusion/Base/MemImage.h>
#include <ImFusion/Base/SharedImage.h>
#include <ImFusion/Base/SharedImageSet.h>

#include <Windows.h>

namespace ImFusion
{
	LoggerAlgorithm::LoggerAlgorithm(SharedImageSet* img)
		: m_imgIn(img)
	{
	}


	bool LoggerAlgorithm::createCompatible(const DataList& data, Algorithm** a)
	{
		// check requirements to create the algorithm
		if (data.size() != 1)
			return false;
		SharedImageSet* img = data.getImage(Data::UNKNOWN);    // in our case, any image is fine
		if (img == nullptr)
			return false;

		// requirements are met, create the algorithm if asked
		if (a)
		{
			*a = new LoggerAlgorithm(img);
			(*a)->setInput(data);
		}
		return true;
	}


	void LoggerAlgorithm::compute()
	{
		// set generic error status until we have finished
		m_status = static_cast<int>(Status::Error);

		m_imgOut = std::make_unique<SharedImageSet>();

		std::string iflog = "C://Users//Jorgue Guerra//AppData//Roaming//ImFusion//ImFusion Suite//ImFusionSuite.log";
		LOG_INFO("[SIRT][LOGGER] Save folder: " << iflog);
		LOG_INFO("[SIRT][LOGGER] " << m_message);

		std::string filename = "C://Master thesis//master//imfusion-plugin//logger.log";
		Log::init(true, true, filename);
		Log::log(Log::Info, "", "Log flushed");

		int delay = 10;
		for(int i = 0; i < delay; i++)
		{
			LOG_INFO(delay - i);
			Sleep(1000);
		}
		m_status = static_cast<int>(Status::Success);
	}


	void LoggerAlgorithm::output(DataList& dataOut)
	{
	}


	void LoggerAlgorithm::configure(const Properties* p)
	{
		// this method restores our members when a workspace file is loaded
		if (p == nullptr)
			return;

		p->param("message", m_message);
		for (int i = 0; i < (int)m_listeners.size(); ++i)
			m_listeners[i]->algorithmParametersChanged();
	}


	void LoggerAlgorithm::configuration(Properties* p) const
	{
		// this method is necessary to store our settings in a workspace file
		if (p == nullptr)
			return;

		p->setParam("message", m_message, "");
	}
}
