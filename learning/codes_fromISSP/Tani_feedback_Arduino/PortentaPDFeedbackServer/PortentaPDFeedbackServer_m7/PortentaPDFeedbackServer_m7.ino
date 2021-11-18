#include "Arduino.h"
#include "RPC_internal.h"
#include <WiFi.h>
//#include <FlashStorage.h>
#include "arduino_secrets.h"
#include "js.h"
#include "css.h"
#define FULL_COUNT 143360

signed int zeroPos = 0;
signed int stagePos = 0;
bool feedbackState = false;
unsigned long prevPosUpdateTime = 0;
char buf[20] = {0};
bool stepSizeAdjusted = false;

//FlashStorage(storage_zeroPos, signed int);

///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = SECRET_SSID;    // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;             // your network key Index number (needed only for WEP)
using namespace rtos;

int status = WL_IDLE_STATUS;

WiFiServer server(80);
Thread elliptecThread;

void setup() {
  // put your setup code here, to run once:
  bootM4();
  Serial.begin(9600);
  Serial1.begin(9600);
  
  
  RPC1.begin();
  Serial.println("Access Point Web Server");

  // by default the local IP address of will be 192.168.3.1
  // you can override it with the following:
  // WiFi.config(IPAddress(10, 0, 0, 1));

  if(strlen(pass) < 8){    
    Serial.println("Creating access point failed");
    Serial.println("The Wi-Fi password must be at least 8 characters long");
    // don't continue
    while(true);
  }
    
  // print the network name (SSID);
  Serial.print("Creating access point named: ");
  Serial.println(ssid);

  //Create the Access point
  status = WiFi.beginAP(ssid,pass);
  if(status != WL_AP_LISTENING){
    Serial.println("Creating access point failed");
    // don't continue
    while (true);
  }

  // wait 10 seconds for connection:
  delay(10000);

  // start the web server on port 80
  server.begin();
  
//  zeroPos = storage_zeroPos.read();
  Serial.print("Zero pos:");
  Serial.println(zeroPos);

  printWiFiStatus();
  elliptecThread.start(elliptecThreadFunc);

  checkStatus();
  delay(100);
  backToHome();
  delay(500);
  checkStatus();
  delay(100);
  while(!stepSizeAdjusted) {
    setJogSize();
    delay(200);
  }
  setPowerRatio(0);
}

void loop() {
  String data = "";
  String response = "";
  float value_f = 0;
  if (status != WiFi.status()) {
    status = WiFi.status();
    if (status == WL_AP_CONNECTED) {
      Serial.println("Device connected to AP");
    } else {
      Serial.println("Device disconnected from AP");
    }
  }
  WiFiClient client = server.available();  
  if (client) {                             
    String currentLine = ""; 
  
    while (client.connected()) {            
      if (client.available()) {            
        char c = client.read();
        if (c == '\n') {            
          if (currentLine.length() == 0) {
            break;
          }
          if(currentLine.startsWith("GET /")) {
            int index;
            currentLine.replace("GET /", "");
            index = currentLine.indexOf(" ");
            currentLine = currentLine.substring(0, index);
            if (currentLine.length() == 0) {
              client.println("HTTP/1.1 200 OK");
              client.println("Content-type:text/html");
              client.println();
              client.print("<html><head>");
              client.print("<title>11 eV power controller</title>");
              client.print("<script>");
              client.print(js_str);
              client.print("</script>");
              client.print("<style>");
              client.print(css_str);
              client.print("</style>");
              client.print("<style>");
              client.print("* { font-family: sans-serif;}");
              client.print("body { padding: 2em; font-size: 2em; text-align: center;}");            
              client.print("</style></head>");
              client.print("<body><h2> Current Power </h2>");
              client.print("<p id='value' style='font-size:48px;'> - </p>");
              client.print("<button onclick='set_target()' style='width:80%;'>Set the value as the target.</button>");
              client.print("<h2><span>Power Control </span></h2>");
              client.print("<button onclick='change_power(0)'>0%</button>");
              client.print("<button onclick='change_power(1)'>100%</button></br>");
              client.print("<button onclick='change_power(0.03)' style='width:25%;'>3%</button>");
              client.print("<button onclick='change_power(0.1)' style='width:25%;'>10%</button>");
              client.print("<button onclick='change_power(0.95)' style='width:25%;'>95%</button></br>");
             
              client.print("<h2><span>Feedback</span></h2>");
              client.print("<button onclick='turn_feedback(\"on\")'>ON</button>");
              client.print("<button onclick='turn_feedback(\"off\")'>OFF</button>");
             
              client.print("</body></html>");
              client.println();
            } else if (currentLine.startsWith("feedback/")) {
              currentLine.replace("feedback/", "");
              if (currentLine.startsWith("on")) {
                RPC1.println("start");
                RPC1.flush();
                feedbackState = true;
              } else {
                RPC1.println("stop");
                RPC1.flush();
                feedbackState = false;
              }
            } else if (currentLine.startsWith("power/") && !feedbackState) {
              currentLine.replace("power/", "");
              float f;
              f = currentLine.toFloat();
              f = f > 1 ? 1 : (f < 0 ? 0 : f);
              setPowerRatio(f);
              Serial.println(f);
            } else if (currentLine.startsWith("set_pos/") && !feedbackState) {
              currentLine.replace("set_pos/", "");
              unsigned int pos;
              pos = currentLine.toInt();
              sprintf(buf, "0ma%08X", pos);
              Serial1.print(buf);
              Serial1.flush();
              client.println("HTTP/1.1 200 OK");
              client.println("Content-type:application/json");
              client.println();
              client.print("{\"position\":");
              client.print(pos);
              client.print("}");
              client.println();
              client.flush();
            } else if (currentLine.startsWith("set_target")) {
              RPC1.println("set");
              RPC1.flush();
            } else if (currentLine.startsWith("voltage")) {
              RPC1.println("voltage");
              RPC1.flush();
              value_f = readRPC().toFloat();
              client.println("HTTP/1.1 200 OK");
              client.println("Content-type:application/json");
              client.println();
              client.print("{\"voltage\":");
              client.print(value_f, 4);
              client.print("}");
              client.println();
              client.flush();
            } else if (currentLine.startsWith("history")) {
              int index = 0;
              String reply;
              RPC1.println("history");
              RPC1.flush();
              client.println("HTTP/1.1 200 OK");
              client.println("Content-type:application/json");
              client.println();
              client.print("{\"history\":[");
              Serial.println("HISTORY");
              while(1) {
                reply = readRPC();
                
                if (reply == "end") {
                  break;
                }
                if (reply.length() >= 1) {
                  Serial.println(reply);
                  if (index % 2 == 1) {
                    if (index >= 2) {
                      client.print(",");
                    }
                    client.print(reply);
                  }
                  index++;
                }
              }
              client.print("]}");
              client.println();
              client.flush();
            }
          }
          currentLine = "";
          break;
        } else if (c != '\r') {    // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }
      }
    }
    // close the connection:
    client.stop();
  }
  delay(1);
}


void printWiFiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your Wi-Fi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print where to go in a browser:
  Serial.print("To see this page in action, open a browser to http://");
  Serial.println(ip);
}


String readRPC() {
  String data = "";
  while (RPC1.available()) {
    data += (char)RPC1.read();
    if (data.endsWith("\r\n")) {
      break;
    }
  }
  data.trim();
  return data;
}

String sendElliptecCommand(String command) {
  Serial1.print(command);
  Serial1.flush();
  return "";
}

void elliptecThreadFunc() {
  while(true) {
    delay(50);
    processElliptecSerial();
  }
}
void processElliptecSerial() {
  String reply;
  reply = readALine();
  if (reply == "") {
    return;
  }
  if (reply.startsWith("0PO") || reply.startsWith("0BO")) {
    reply = reply.substring(3);
    if (reply.length() == 8) {
      unsigned long ul = strtoul(reply.c_str(), NULL, 16);
      stagePos = strtoul(reply.c_str(), NULL, 16);
      if(ul > 0x80000000) {
        stagePos = -(signed int)(0xFFFFFFFF - stagePos);
      } else {
        stagePos = ul;
      }
      Serial.print(" ---> ");
      Serial.println(stagePos);
      if(millis() - prevPosUpdateTime > 500) {
        RPC1.print("stage:");
        RPC1.println(stagePos);
        RPC1.flush();
        prevPosUpdateTime = millis();
      }
    }
  }
  if (reply.startsWith("0GJ")) {
    stepSizeAdjusted = true;
  }
}

String readALine() {
  String reply = "";
  while (Serial1.available()) {
    reply += (char)Serial1.read();
    if (reply.endsWith("\r\n")) {
      break;
    }
    delay(1);
  }
  reply.trim();
  if(reply != "") {
    Serial.println(reply);
  }
  return reply;
}

bool checkStatus() {
  String reply = sendElliptecCommand("0gs");
  return true;
}

unsigned long getPosition() {
  String reply = sendElliptecCommand("0gp").substring(3);
  long b = strtol(reply.c_str(), NULL, 16);
  return b;
}

void backToHome() {
  String reply = sendElliptecCommand("0ho0");
}

bool setPowerRatio(float ratio) {
  unsigned int pos = asin(ratio)/(3.141592/2.0)*FULL_COUNT/8;
  Serial.print("power:");
  Serial.println(pos);
  pos += zeroPos;
  sprintf(buf, "0ma%08X", pos);
  Serial1.print(buf);
  Serial1.flush();
  Serial.println(buf);
  return true;
}

void setJogSize() {

  Serial1.print("0sj00000005");
  Serial1.flush();
  delay(100);
  sendElliptecCommand("0gj");
  delay(100);
  checkStatus();
}
