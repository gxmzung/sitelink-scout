#include <Arduino.h>
#include <HTTPClient.h>
#include <WiFi.h>

#include "api_client.h"
#include "config.h"


bool connectTransportWiFi() {
    if (WiFi.status() == WL_CONNECTED) {
        return true;
    }

    Serial.println();
    Serial.println("[WiFi] Connecting...");
    Serial.print("[WiFi] SSID: ");
    Serial.println(WIFI_SSID);

    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    unsigned long startedAt = millis();

    while (
        WiFi.status() != WL_CONNECTED &&
        millis() - startedAt < WIFI_CONNECT_TIMEOUT_MS
    ) {
        delay(500);
        Serial.print(".");
    }

    Serial.println();

    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("[WiFi] Connection failed");
        return false;
    }

    Serial.println("[WiFi] Connected");
    Serial.print("[WiFi] ESP32 IP: ");
    Serial.println(WiFi.localIP());

    return true;
}


bool sendMeasurement(const WiFiMeasurement& measurement) {
    if (!measurement.found) {
        Serial.println("[API] Skip: target AP not found");
        return false;
    }

    if (!connectTransportWiFi()) {
        Serial.println("[API] Skip: transport Wi-Fi unavailable");
        return false;
    }

    HTTPClient http;

    if (!http.begin(API_URL)) {
        Serial.println("[API] http.begin failed");
        return false;
    }

    http.addHeader("Content-Type", "application/json");

    String payload = "{";

    payload += "\"device_id\":\"";
    payload += SCOUT_DEVICE_ID;
    payload += "\",";

    payload += "\"zone_id\":\"";
    payload += SCOUT_ZONE_ID;
    payload += "\",";

    payload += "\"ssid\":\"";
    payload += measurement.ssid;
    payload += "\",";

    payload += "\"bssid\":\"";
    payload += measurement.bssid;
    payload += "\",";

    payload += "\"rssi\":";
    payload += String(measurement.rssi);
    payload += ",";

    payload += "\"channel\":";
    payload += String(measurement.channel);

    payload += "}";

    Serial.println();
    Serial.println("[API] POST measurement");
    Serial.print("[API] URL: ");
    Serial.println(API_URL);

    Serial.print("[API] Payload: ");
    Serial.println(payload);

    int httpCode = http.POST(payload);

    if (httpCode <= 0) {
        Serial.print("[API] POST failed: ");
        Serial.println(http.errorToString(httpCode));

        http.end();
        return false;
    }

    String response = http.getString();

    Serial.print("[API] HTTP ");
    Serial.println(httpCode);

    Serial.print("[API] Response: ");
    Serial.println(response);

    bool success = (
        httpCode >= 200 &&
        httpCode < 300
    );

    http.end();

    return success;
}
