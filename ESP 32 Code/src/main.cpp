#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "JJ";
const char* password = "20010130";

const char* mqtt_server = "192.168.110.199";
const int mqtt_port = 1883;
const char* mqtt_client_id = "testing";

// MQTT topics
const char* mqtt_topic_rssi = "rssi/data";
const char* mqtt_topic_command = "command";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  
  // Connect to WiFi network
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Connect to MQTT broker
  client.setServer(mqtt_server, mqtt_port);
  while (!client.connected()) {
    if (client.connect(mqtt_client_id)) {
      Serial.println("Connected to MQTT broker");
    } else {
      delay(5000);
      Serial.println("Failed to connect to MQTT broker, retrying...");
    }
  }
}

void loop() {
  // Scan for APs
  int n = WiFi.scanNetworks();
  for (int i = 0; i < n; ++i) {
    // Get RSSI and MAC address
    String ssid = WiFi.SSID(i);
    String rssi = String(WiFi.RSSI(i));
    String mac = WiFi.BSSIDstr(i);

    // Publish RSSI and MAC address to MQTT broker
    String payload = "SSID: " + ssid + ", MAC: " + mac + ", RSSI: " + rssi;
    client.publish(mqtt_topic_rssi, payload.c_str());
  }

  delay(5000);  // Scan every 5 seconds
}
