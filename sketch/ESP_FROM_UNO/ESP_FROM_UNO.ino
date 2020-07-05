#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <SoftwareSerial.h>
//Constants
const char* ssid = "TECNO CAMON 11";                                                                       // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "91111111";                                                           // The password of the Wi-Fi network
const char server[] = "http://healthapp-v1.herokuapp.com";                                     //Change this value for each room, must match the model field
const String connector = "http://healthapp-v1.herokuapp.com/patient/upload/vitals/";            //Port must be in URL

int tempPin = A0;

SoftwareSerial mySerial(D2, D3); // RX, TX

//String serial_data;
const String device = "2345453ds3";
//{
//  "device_serial_number":"2345453ds3",
//  "pulse_bpm":"85",
//  "temperature": "35"
//}

WiFiClient client;
HTTPClient http;

void setup() {
  Serial.begin(9600);
  mySerial.begin(115200);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid,password);
  Serial.print("Connecting...");
  open_connection();

  Serial.println('\n');
  Serial.println("Attempting to connect to server...");
  if (client.connect(server, 443)){
    Serial.println("Connected to server!");
  } else{
    Serial.println("Failed to connect :(");
    Serial.println("");
    return;
  }

}

void loop() {

  if(WiFi.status()==WL_CONNECTED) {
    if (mySerial.available() > 0){
      //if(client.connect(server, 443)){
          commit_pulse_reading();
        //}
      
    }else{
      Serial.println("No data...");
    }
    }else {
    Serial.println("WiFi not connected");
  }
  delay(500); //delays for 30 seconds
}


void open_connection() {
  int i = 0;
  while (WiFi.status() != WL_CONNECTED) { // Wait for the Wi-Fi to connect
    delay(500);
    Serial.print(++i); Serial.print(' ');
  }

  Serial.println('\n');
  Serial.println(" WiFi Connection established!");
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());
}

int read_temp(){
  int temp = analogRead(tempPin);    //Read the analog pin
  temp = temp * 0.48828125; 
  delay(1000);
  return temp;
}

void commit_pulse_reading() {
  
  String PostData;
  String serial_data;
  String serialized_data;
  
  serial_data = mySerial.read(); //reads data from serial
  String tempString = String(read_temp());
  DynamicJsonDocument doc(1024); // ArduinoJson version 6+
  doc["device_serial_number"] = device;
  doc["pulse_bpm"] = serial_data;
  doc["temperature"] = tempString;
  
  char buffer[256];
 
  serialized_data = serializeJson(doc, buffer);
  Serial.println(buffer);
  
//  serialized_data = serializeJsonPretty(doc, Serial); //json format
//  Serial.println(http.begin(client,connector)); 
  //Send data to API
  if (http.begin(client,connector)) {
    PostData = buffer;
//    Serial.println(PostData);
    http.begin(client,connector);
    http.addHeader("Content-Type", "application/json");
    int httpCode = http.POST(PostData);
//    Serial.println("Sending data to server...");
//    delay(3000);
     if (httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] POST... code: %d\n", httpCode);

      // file found at server
      if (httpCode == HTTP_CODE_OK) {
        const String& payload = http.getString();
        Serial.println("received payload:\n<<");
        Serial.println(payload);
        Serial.println(">>");
      }
    } else {
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
    if(String(Serial.println(http.getString())) == String("")) {
      Serial.println("Failed to send data...");
      }
    } else {
      
      Serial.println("Failed to send data...");
      }

}
