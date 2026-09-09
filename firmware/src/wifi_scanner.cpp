#include <WiFi.h>

#include "wifi_scanner.h"

SignalStatus classifySignal(const int32_t rssi) {
    if (rssi >= -55) {
        return SignalStatus::EXCELLENT;
    }

    if (rssi >= -65) {
        return SignalStatus::GOOD;
    }

    if (rssi >= -75) {
        return SignalStatus::FAIR;
    }

    if (rssi >= -85) {
        return SignalStatus::POOR;
    }

    return SignalStatus::DEAD;
}

const char* signalStatusToString(const SignalStatus status) {
    switch (status) {
        case SignalStatus::EXCELLENT:
            return "EXCELLENT";

        case SignalStatus::GOOD:
            return "GOOD";

        case SignalStatus::FAIR:
            return "FAIR";

        case SignalStatus::POOR:
            return "POOR";

        case SignalStatus::DEAD:
        default:
            return "DEAD";
    }
}

WiFiMeasurement scanTargetNetwork(
    const char* targetSsid,
    const char* targetBssid
) {
    WiFiMeasurement result;

    WiFi.mode(WIFI_STA);
    WiFi.disconnect(false, false);
    delay(100);

    const int networkCount = WiFi.scanNetworks(
        false,
        true
    );

    if (networkCount <= 0) {
        WiFi.scanDelete();
        return result;
    }

    for (int i = 0; i < networkCount; ++i) {
        const String ssid = WiFi.SSID(i);
        const String bssid = WiFi.BSSIDstr(i);

        const bool ssidMatches =
            ssid == targetSsid;

        const bool bssidMatches =
            targetBssid == nullptr ||
            strlen(targetBssid) == 0 ||
            bssid.equalsIgnoreCase(targetBssid);

        if (!ssidMatches || !bssidMatches) {
            continue;
        }

        // Same SSID may exist on multiple APs.
        // Keep the strongest matching AP.
        if (!result.found || WiFi.RSSI(i) > result.rssi) {
            result.found = true;
            result.ssid = ssid;
            result.bssid = bssid;
            result.rssi = WiFi.RSSI(i);
            result.channel = WiFi.channel(i);
        }
    }

    WiFi.scanDelete();

    return result;
}
