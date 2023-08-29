#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>
#include <SPI.h>
#include <MFRC522.h>
#include <FirebaseESP8266.h>
#include <ESP8266WiFi.h>
#include <map>

FirebaseData firebaseData;
FirebaseJson json;

#define FIREBASE_HOST "https://smartcart-c354c-default-rtdb.europe-west1.firebasedatabase.app"
#define FIREBASE_AUTH "n2M0sZrQkwGNtqAo8bktz4kptwy6G1nMLp2aZGg8"
#define ssid "Vignesh"
#define password "123456789"

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SDA_PIN D3 // RX
#define SCL_PIN D1 // TX

#define RST_PIN_1 D0
#define RST_PIN_2 D4
#define SS_PIN_1 D8
#define SS_PIN_2 D2

MFRC522 rfid1(SS_PIN_1, RST_PIN_1);
MFRC522 rfid2(SS_PIN_2, RST_PIN_2);

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
String uid_prev = "";

std::map<String, String> products = {
  {"43835fa7", "MILK"},
  {"22919e39", "BREAD"},
  {"3029e51c", "EGGS"},
  {"91414b20", "SNACKS"},
  {"6265cf1b", "CHOCOLATE"},
  {"76635430", "SOAP"},
  {"139b5191", "PERFUME"}
};

void setup() {
  Serial.begin(9600); // Initialize Serial for debugging
  Wire.begin(SDA_PIN, SCL_PIN);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    for (;;);
  }

  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
WiFi.begin(ssid, password);
  SPI.begin();
  rfid1.PCD_Init();
  rfid2.PCD_Init();

  printOnOled("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
  Serial.println("WiFi connected"); // Debug print
  printOnOled("WiFi connected");

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

  printOnOled("Connected to Firebase");
}

void loop() {
  Firebase.reconnectWiFi(true);
  scanRFID(&rfid1, "/cart2/remove");
  scanRFID(&rfid2, "/cart2/add");
  delay(1000);
}

void scanRFID(MFRC522* rfid, const String& path) {
  if (!rfid->PICC_IsNewCardPresent() || !rfid->PICC_ReadCardSerial())
    return;

  String uid = "";
  for (byte i = 0; i < rfid->uid.size; i++) {
    uid += rfid->uid.uidByte[i] < 0x10 ? "0" : "";
    uid += String(rfid->uid.uidByte[i], HEX);
  }

  rfid->PICC_HaltA();
  rfid->PCD_StopCrypto1();

  if (products.count(uid) > 0 && uid != uid_prev) {
    Serial.println("Scanned UID: " + uid); // Debug print
    printOnOled(products[uid]);
    json.clear();
    json.set("product", products[uid]); 
    json.set("uid", uid);
    if (Firebase.pushJSON(firebaseData, path, json)) {
      Serial.println("Data pushed to Firebase successfully.");
    } else {
      Serial.println("Failed to push data to Firebase.");
      Serial.println("Error: " + firebaseData.errorReason()); // Print the error reason
    }
    uid_prev = uid;
  }
}

void printOnOled(String message) {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println(message);
  display.display();
}
