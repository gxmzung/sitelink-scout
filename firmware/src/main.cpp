#include <Arduino.h>
#include <WiFi.h>

static constexpr char DEVICE_ID[] = "SCOUT-01";
static constexpr char ZONE_ID[] = "ZONE-B03";

void printNetworkInfo(
    const String& ssid,
    int32_t rssi,
    int32_t channel,
    const String& bssid
) {
    Serial.println("--------------------------------");
    Serial.printf("Device  : %s\n", DEVICE_ID);
    Serial.printf("Zone    : %s\n", ZONE_ID);
    Serial.printf("SSID    : %s\n", ssid.c_str());
    Serial.printf("BSSID   : %s\n", bssid.c_str());
    Serial.printf("RSSI    : %ld dBm\n", static_cast<long>(rssi));
    Serial.printf("Channel : %ld\n", static_cast<long>(channel));
}

void scanNetworks() {
    Serial.println();
    Serial.println("[SiteLink Scout] Starting Wi-Fi scan...");

    WiFi.mode(WIFI_STA);
    WiFi.disconnect(true);
    delay(100);

    const int networkCount = WiFi.scanNetworks();

    if (networkCount <= 0) {
        Serial.println("[Scout] No Wi-Fi networks found.");
        WiFi.scanDelete();
        return;
    }

    Serial.printf("[Scout] %d networks found\n", networkCount);

    for (int i = 0; i < networkCount; ++i) {
        printNetworkInfo(
            WiFi.SSID(i),
            WiFi.RSSI(i),
            WiFi.channel(i),
            WiFi.BSSIDstr(i)
        );
    }

    WiFi.scanDelete();
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    Serial.println();
    Serial.println("================================");
    Serial.println(" SiteLink Scout v0.1.0");
    Serial.println(" Wi-Fi Coverage Validation Node");
    Serial.println("================================");

    scanNetworks();
}

void loop() {
    delay(10000);
    scanNetworks();
}
