#pragma once

#include <Arduino.h>

struct WiFiMeasurement {
    bool found = false;

    String ssid;
    String bssid;

    int32_t rssi = -127;
    int32_t channel = 0;
};

enum class SignalStatus {
    EXCELLENT,
    GOOD,
    FAIR,
    POOR,
    DEAD
};

SignalStatus classifySignal(int32_t rssi);
const char* signalStatusToString(SignalStatus status);
