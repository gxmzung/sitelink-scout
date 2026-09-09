#pragma once

// ============================================================
// SiteLink Scout - Example Configuration
// Copy this file to:
//   firmware/include/config.h
//
// Never commit config.h if it contains real Wi-Fi credentials.
// ============================================================

// Scout identity
#define SCOUT_DEVICE_ID "SCOUT-01"
#define SCOUT_ZONE_ID   "ZONE-B03"

// Target AP to measure
// ESP32 classic models support 2.4 GHz Wi-Fi.
#define TARGET_SSID "SiteLink_AP_01"

// Optional.
// Leave empty to select the strongest AP with TARGET_SSID.
#define TARGET_BSSID ""

// Transport Wi-Fi used to send measurements to FastAPI.
#define WIFI_SSID "YOUR_2_4GHZ_WIFI"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// Mac / backend LAN IP.
// Do not use 127.0.0.1 from the ESP32.
#define API_URL "http://192.168.x.x:8000/api/v1/measurements"

// Timing
#define SCAN_INTERVAL_MS 5000
#define WIFI_CONNECT_TIMEOUT_MS 15000
