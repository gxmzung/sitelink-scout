#pragma once

#include "measurement.h"

bool connectTransportWiFi();
bool sendMeasurement(const WiFiMeasurement& measurement);
