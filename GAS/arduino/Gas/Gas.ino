#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Testgas";
const char* password = "mothaiba";
const char* serverName = "http://192.168.212.179:5000/alert";

const int gasPin = 34;     // Chân cảm biến MQ-5
const int relayPin = 5;    // Chân relay điều khiển quạt
const int buzzerPin = 18;  // Chân buzzer chủ động
const int threshold = 750;

void setup() {
  Serial.begin(115200);
  pinMode(relayPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(relayPin, LOW);  // Tắt quạt ban đầu
  digitalWrite(buzzerPin, LOW); // Tắt còi ban đầu

  WiFi.begin(ssid, password);
  Serial.print("Đang kết nối WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ Đã kết nối WiFi!");
}

void loop() {
  int gasValue = analogRead(gasPin);
  Serial.print("Gas Level: ");
  Serial.println(gasValue);

  if (gasValue > threshold) {
    digitalWrite(relayPin, HIGH);   // Bật quạt
    digitalWrite(buzzerPin, HIGH);  // Bật còi liên tục
    Serial.println("⚠️ Gas detected! Fan ON, Buzzer ON");

    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(serverName);
      http.addHeader("Content-Type", "application/json");

      String json = "{\"gas_value\": " + String(gasValue) + "}";
      int httpResponseCode = http.POST(json);

      Serial.print("Gửi cảnh báo: ");
      Serial.println(httpResponseCode);

      http.end();
    }
  } else {
    digitalWrite(relayPin, LOW);    // Tắt quạt
    digitalWrite(buzzerPin, LOW);   // Tắt còi
  }

  delay(5000); // Kiểm tra mỗi 5 giây
}
