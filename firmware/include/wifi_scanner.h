#pragma once

#include <Arduino.h>
#include "measurement.h"

WiFiMeasurement scanTargetNetwork(
    const char* targetSsid,
    const char* targetBssid = nullptr
);
