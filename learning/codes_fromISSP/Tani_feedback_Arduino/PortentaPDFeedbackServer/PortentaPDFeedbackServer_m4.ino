#include "Arduino.h"
#include "RPC_internal.h"

#define HISTORY_SIZE 10
#define RECORD_INTERVAL 1000
#define FULL_COUNT 143360
#define AVG_COUNT 2000
const int pdPin = A0;
bool controlFlag = false;
float voltage = 0;
float targetVoltage = 0.05;
long count = 0;
long zeroPos = 0;
char buf[20];
float powerRatio = 0;
float tolerence = 0.001;
long prevMoveTime = 0;
long stagePos = 0;
float history[HISTORY_SIZE] = {0.0};
unsigned long history_t[HISTORY_SIZE] = {0};
unsigned int historyIndex = 0;

void setup() {
  analogReadResolution(16);
//  analogReference(EXTERNAL);
  
  
  pinMode(LEDR,OUTPUT);
  pinMode(LEDG,OUTPUT);
  pinMode(LEDB,OUTPUT); 
  pinMode(D12, INPUT); // in-motion
  pinMode(D11, OUTPUT); // jog
  pinMode(D10, OUTPUT); // backward
  pinMode(D9, OUTPUT); // forward
  
  RPC1.begin();
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, LOW);
  digitalWrite(LEDB, HIGH);

  digitalWrite(D11, HIGH); // jog
  digitalWrite(D10, HIGH); // backward
  digitalWrite(D9, HIGH); // forward
}

void loop() {
  // put your main code here, to run repeatedly:
  processCommand();
  delay(1);
  voltage = getVoltage(AVG_COUNT);
  if(millis() - history_t[(historyIndex-1+HISTORY_SIZE) % HISTORY_SIZE] >= RECORD_INTERVAL) {
    history[historyIndex] = voltage;
    history_t[historyIndex] = millis();
    historyIndex = (historyIndex +1) % HISTORY_SIZE;
  }
  
  delay(1);
  if (controlFlag) {
    if(voltage-targetVoltage < -tolerence) {
      rotate(1);
    } else if (voltage-targetVoltage > tolerence) {
      rotate(0);
    }
  }
  delay(1);
}

float getVoltage(int avg_count) {
  int i;
  long value = 0;
  for(i = 0; i < avg_count; i++) {
    value += analogRead(pdPin);
  }
  return (float)value / avg_count / 65536.0;
}

void rotate(int d) {
  if(millis() - prevMoveTime >= 100) {
    prevMoveTime = millis();
    if (d && stagePos >= zeroPos + FULL_COUNT/8) {
      return;
    }
    if (!d && stagePos <= zeroPos) {
      return;
    }
    digitalWrite(D11, LOW);
    delay(1);
    digitalWrite(d ? D9 : D10, LOW);
    delay(1);
    digitalWrite(d ? D9 : D10, HIGH);
    delay(1);
    digitalWrite(D11, HIGH);
    
    stagePos += d ? 10 : -10;
  }
}

void processCommand() {
  String command = readRPC();
  if (command == "") {
    return;
  }
  if (command == "start") {
    controlFlag = true;
    digitalWrite(LEDG, LOW);
    digitalWrite(LEDB, LOW);
  }
  if (command == "stop") {
    controlFlag = false;
    digitalWrite(LEDG, LOW);
    digitalWrite(LEDB, HIGH);
  }
  if (command == "set") {
    targetVoltage = voltage;
  }
  if (command == "voltage") {
    digitalWrite(LEDR, LOW);
    RPC1.println(voltage, 4);
    RPC1.flush();
    digitalWrite(LEDR, HIGH);
  }
  if (command == "history") {
    long i;
    digitalWrite(LEDR, LOW);
    delay(1);
    for(i = 0; i < HISTORY_SIZE; i++) {
      RPC1.println(history_t[i]);
      RPC1.println(history[i], 4);
      delay(1);
    }
    RPC1.println("end");
    RPC1.flush();
    digitalWrite(LEDR, HIGH);
  }
  if (command.startsWith("stage:")) {
    command = command.substring(6);
    stagePos = strtol(command.c_str(), NULL, 10);
  }
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

bool setPowerRatio(float ratio) {
  unsigned int pos = asin(ratio)*65536;
  pos += zeroPos;
  sprintf(buf, "0ma%08X", pos);
  Serial.print(buf);
  powerRatio = ratio;
  return true;
}
