#include <Arduino.h>

#include "measurement.h"
#include "wifi_scanner.h"

static constexpr char DEVICE_ID[] = "SCOUT-01";
static constexpr char ZONE_ID[] = "ZONE-B03";

static constexpr char TARGET_SSID[] = "SiteLink_AP_01";

// Empty string = accept any BSSID with TARGET_SSID.
// Later this can be set to a specific AP MAC address.
static constexpr char TARGET_BSSID[] = "";

static constexpr uint32_t SCAN_INTERVAL_MS = 5000;

void printMeasurement(const WiFiMeasurement& measurement) {
    Serial.println();
    Serial.println("--------------------------------");

    Serial.printf("Device  : %s\n", DEVICE_ID);
    Serial.printf("Zone    : %s\n", ZONE_ID);

    if (!measurement.found) {
        Serial.printf("SSID    : %s\n", TARGET_SSID);
        Serial.println("Status  : NOT FOUND");
        return;
    }

    const SignalStatus status =
        classifySignal(measurement.rssi);

    Serial.printf(
        "SSID    : %s\n",
        measurement.ssid.c_str()
    );

    Serial.printf(
        "BSSID   : %s\n",
        measurement.bssid.c_str()
    );

    Serial.printf(
        "RSSI    : %ld dBm\n",
        static_cast<long>(measurement.rssi)
    );

    Serial.printf(
        "Channel : %ld\n",
        static_cast<long>(measurement.channel)
    );

    Serial.printf(
        "Status  : %s\n",
        signalStatusToString(status)
    );
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    Serial.println();
    Serial.println("================================");
    Serial.println(" SiteLink Scout v0.1.0");
    Serial.println(" Target AP Measurement Node");
    Serial.println("================================");

    Serial.printf("Device ID   : %s\n", DEVICE_ID);
    Serial.printf("Zone ID     : %s\n", ZONE_ID);
    Serial.printf("Target SSID : %s\n", TARGET_SSID);
}

void loop() {
    const WiFiMeasurement measurement =
        scanTargetNetwork(
            TARGET_SSID,
            TARGET_BSSID
        );

    printMeasurement(measurement);

    delay(SCAN_INTERVAL_MS);
}
