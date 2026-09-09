#include <Arduino.h>
#include <WiFi.h>

#include "api_client.h"
#include "config.h"
#include "measurement.h"
#include "wifi_scanner.h"


unsigned long lastScanAt = 0;


void printMeasurement(
    const WiFiMeasurement& measurement
) {
    Serial.println();
    Serial.println("================================");
    Serial.println(" SiteLink Scout Measurement");
    Serial.println("================================");

    if (!measurement.found) {
        Serial.print("Target SSID: ");
        Serial.println(TARGET_SSID);

        Serial.println("Result: NOT FOUND");
        Serial.println("================================");
        return;
    }

    Serial.print("Device: ");
    Serial.println(SCOUT_DEVICE_ID);

    Serial.print("Zone: ");
    Serial.println(SCOUT_ZONE_ID);

    Serial.print("SSID: ");
    Serial.println(measurement.ssid);

    Serial.print("BSSID: ");
    Serial.println(measurement.bssid);

    Serial.print("RSSI: ");
    Serial.print(measurement.rssi);
    Serial.println(" dBm");

    Serial.print("Channel: ");
    Serial.println(measurement.channel);

    Serial.println("================================");
}


void setup() {
    Serial.begin(115200);

    delay(1000);

    Serial.println();
    Serial.println("================================");
    Serial.println(" SiteLink Scout");
    Serial.println(" Real Measurement Transport");
    Serial.println("================================");

    WiFi.mode(WIFI_STA);

    connectTransportWiFi();

    Serial.println();
    Serial.println("[Scout] Ready");
}


void loop() {
    if (
        lastScanAt == 0 ||
        millis() - lastScanAt >= SCAN_INTERVAL_MS
    ) {
        lastScanAt = millis();

        WiFiMeasurement measurement =
            scanTargetNetwork(
                TARGET_SSID,
                TARGET_BSSID
            );

        printMeasurement(measurement);

        if (measurement.found) {
            bool sent =
                sendMeasurement(measurement);

            Serial.print("[Scout] Upload: ");
            Serial.println(
                sent ? "SUCCESS" : "FAILED"
            );
        }
    }

    delay(50);
}
