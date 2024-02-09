#include <SoftwareSerial.h>
#include <TinyGPS.h>
#include "WiFiS3.h"
#include <ArduinoJson.h>
#include <EEPROM.h>


//////////////////////////////////////////////////////////////////////////////////////////////////////////////

//per connessione a server
const char *serverAddress = "155.185.91.16";
const int serverPort = 8080;

char ssid[] = "iPhone di Matteo";        // your network SSID (name)
char pass[] = "pippoooo";    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;            // your network key index number (needed only for WEP)

int status = WL_IDLE_STATUS;
// if you don't want to use DNS (and reduce your sketch size)
// use the numeric IP instead of the name for the server:
//IPAddress server(74,125,232,128);  // numeric IP for Google (no DNS)
char server[] = "www.google.com";    // name address for Google (using DNS)

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
WiFiClient client;

//////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Configura i pin RX e TX per il modulo GPS e GSM
SoftwareSerial gpsSerial(10, 11);  // RX, TX per il modulo GPS
SoftwareSerial gsmSerial(2,3);    // RX, TX per il modulo GSM
TinyGPS gps;

//Identificativo dispositivo
uint8_t signature= EEPROM.read(0);
 

String phoneNumberList = "";  // Lista numeri telefonici
const int sogliaFumo = 100, sogliaTemperatura = 100, sogliaUmidita = 100;  // Soglia dai tuoi sensori per l'invio della posizione

// Simula la lettura dai sensori (da sostituire con la logica reale)
int valoreFumo = 120, valoreTemperatura = 120, valoreUmidita = 120;
int valoreSensore; //da sostituire con valore soglia superato

//funzione per delay efficace
static void smartdelay(unsigned long ms);


void setup() {

  Serial.begin(9600);
  gpsSerial.begin(9600);
  gsmSerial.begin(9600);
  
////////////////////////////////////////////////////////////////////////////////////////
  //connessione wifi
   while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true);
  }
  
  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }
  
  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);
     
    // wait 10 seconds for connection:
    delay(5000);
  
  }

//////////////////////////////////////////////////////////////////////////////////////// fine connessione wifi

Serial.println("prova1");

  // Serial.println("Initializing...");
  // delay(1000);

  // gsmSerial.println("AT"); //Once the handshake test is successful, it will back to OK
  // updateSerial();
  // gsmSerial.println("AT+CSQ"); //Signal quality test, value range is 0-31 , 31 is the best
  // updateSerial();
  // gsmSerial.println("AT+CCID"); //Read SIM information to confirm whether the SIM is plugged
  // updateSerial();
  // gsmSerial.println("AT+CREG?"); //Check whether it has registered in the network
  // updateSerial();

  //   // Verifica la connessione GSM
  // if (checkGSMConnection()) {
  //   Serial.println("Il modulo GSM è correttamente collegato e risponde ai comandi AT.");
  // } else {
  //   Serial.println("Problemi con il modulo GSM. Controlla i collegamenti e l'alimentazione.");
  // }
  
  

  Serial.print("ID del microcontrollore: ");
  Serial.print(signature);
  Serial.print("\n");

  //TESTING DEBUG
  Serial.println("Sats HDOP Latitude  Longitude  Fix  Date       Time     Date Alt    Course Speed Card  Distance Course Card  Chars Sentences Checksum");
  Serial.println("          (deg)     (deg)      Age                      Age  (m)    --- from GPS ----  ---- to London  ----  RX    RX        Fail");
  Serial.println("-------------------------------------------------------------------------------------------------------------------------------------");

  //POST per inizializzare il dispositivo (se già presente la post fallirà)
  serverPost(serverAddress, serverPort, getJsonString(signature, 0,0,0), signature);

  //configurazione GSM
  configureGSM();
  
  // Simula l'inizializzazione della lista numeri dal server (da sostituire con la logica reale)
  phoneNumberList = "+393294494417,3458932894";
}

void loop() {
  float flat, flon;
  unsigned long age, date, time, chars = 0;

  //readGPSData();
  
  //prendiamo tutti i valori dei sensori
  //gps.f_get_position(&flat, &flon, &age);
  
  //dati random
  flat = 37.7749;
  flon = -122.4194;
  age = 60; // 60 secondi

  // Invia i dati al server (sostituire con la logica reale)
  sendDataToServer(signature,flat,flon,age);
 

  // Contatta i numeri telefonici se superata la soglia
  
  //caso umidità
  if (valoreUmidita > sogliaUmidita) {
    //checkServer(flat,flon,age,valoreSensore);
    valoreSensore = valoreUmidita;
    //genera link google maps
    String googleMapsLink = generateGoogleMapsLink(flat, flon);

    String tipo = "Umidità";
    sendLocationToContacts(googleMapsLink, valoreSensore, tipo);
  }

  //caso fumo
  if (valoreFumo > sogliaFumo) {
    //checkServer(flat,flon,age,valoreSensore);
    valoreSensore = valoreFumo;
    //genera link google maps
    String googleMapsLink = generateGoogleMapsLink(flat, flon);

    String tipo = "Fumo";
    sendLocationToContacts(googleMapsLink, valoreSensore, tipo);
  }
  
  //caso temperatura
  if (valoreTemperatura > sogliaTemperatura) {
    //checkServer(flat,flon,age,valoreSensore);
    valoreSensore = valoreTemperatura;
    //genera link google maps
    String googleMapsLink = generateGoogleMapsLink(flat, flon);
  
    String tipo = "Temperatura";
    sendLocationToContacts(googleMapsLink, valoreSensore, tipo);
}

   smartdelay(1000);
}


void updateSerial()
{
  delay(500);
  while (Serial.available()) 
  {
    gsmSerial.write(Serial.read());//Forward what Serial received to Software Serial Port
  }
  while(gsmSerial.available()) 
  {
    Serial.write(gsmSerial.read());//Forward what Software Serial received to Serial Port
  }
}

//configurazione iniziale GSM
void configureGSM() {
  gsmSerial.println("AT");
  delay(2000);
  while (gsmSerial.available()) {
    Serial.write(gsmSerial.read());
  }

  gsmSerial.println("AT+CMGF=1");
  delay(2000);
  while (gsmSerial.available()) {
    Serial.write(gsmSerial.read());
  }
}

//trasforma dati in jSon per trasferimento a server
  String getJsonString (uint8_t signature,float flat,float flon,unsigned long age) {
    
  const size_t capacity = JSON_OBJECT_SIZE(4);
  DynamicJsonDocument doc(capacity);

  // Inserire i dati nell'oggetto JSON
  doc["id"] = signature;
  doc["latitude"] = flat;
  doc["longitude"] = flon;
  doc["temperature"] = age;

  // Serializzare l'oggetto JSON in una stringa
  String jsonString;
  serializeJson(doc, jsonString);
  return jsonString;
  }

//PUT a server
 void serverPut(const char* serverAddress, const int serverPort, String jsonString, uint8_t signature) {
  if (client.connect(serverAddress, serverPort)) {
    client.println("PUT /api/vehicles/" + String(signature) + "/ HTTP/1.1");
    client.println("Host: " + String(serverAddress));
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(jsonString.length());
    client.println();
    client.println(jsonString);

    // Leggere la risposta dal server se necessario
    while (client.available()) {
      char c = client.read();
      Serial.print(c); // Puoi anche ignorare questa parte se non ti interessa la risposta
    }

  }
 }


 bool checkGSMConnection() {
  Serial.println("prova3");
  gsmSerial.println("AT");
  delay(1000);  // Aspetta la risposta del modulo GSM
  Serial.println("prova");
  // Leggi e stampa la risposta del modulo GSM sulla seriale Arduino
  while (gsmSerial.available()) {
    char c = gsmSerial.read();
    Serial.write(c);
  }

  // Verifica se la risposta contiene "OK"
  return gsmSerial.find("OK") != -1;
}


 void serverPost(const char* serverAddress, const int serverPort, String jsonString, uint8_t signature) {
  if (client.connect(serverAddress, serverPort)) {
    client.println("POST /api/vehicles/ HTTP/1.1");
    client.println("Host: " + String(serverAddress));
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(jsonString.length());
    client.println();
    client.println(jsonString);

    // Leggere la risposta dal server se necessario
    while (client.available()) {
      char c = client.read();
      Serial.print(c); // Puoi anche ignorare questa parte se non ti interessa la risposta
    }

  }
 }

String generateGoogleMapsLink(float latitude, float longitude) {
  // Formatta il link di Google Maps
  String link = "https://www.google.com/maps?q=" + String(latitude, 6) + "," + String(longitude, 6);
  return link;
}

void sendDataToServer(uint8_t signature, float flat, float flon, unsigned long age) {

  //print_date(gps);
  // Implementa la logica per inviare i dati al tuo server
  // Usa protocolli come HTTP o MQTT a seconda delle tue esigenze
  // Esempio: invia i dati via HTTP POST

  String jsonString = getJsonString(signature, flat, flon, age);

  serverPut(serverAddress, serverPort, jsonString, signature);


}



void sendSMS(uint8_t signature, String phoneNumber, float sensorValue, String googleMapsLink, String tipo) {
  String message = "Attenzione, la soglia di rischio" + tipo + "è stata superata!\n Link Google Maps: " + googleMapsLink + "\n\nValore del sensore: " + String(sensorValue);

  gsmSerial.println("AT+CMGS=\"" + phoneNumber + "\"");
  delay(1000);
  gsmSerial.println(message);
  delay(1000);
  gsmSerial.println((char)26);
  delay(1000);
}

void sendLocationToContacts(String location,int valoreSensore, String tipo) {
  // Dividi la lista numeri e invia la posizione a ciascun numero
  int commaIndex = phoneNumberList.indexOf(',');
  while (commaIndex != -1) {
    String phoneNumber = phoneNumberList.substring(0, commaIndex);
    sendSMS(signature, phoneNumber, valoreSensore, location, tipo);
    phoneNumberList = phoneNumberList.substring(commaIndex + 1);
    commaIndex = phoneNumberList.indexOf(',');
  }
}



static void smartdelay(unsigned long ms) {
  unsigned long start = millis();
  do 
  {
    while (gpsSerial.available())
      gps.encode(gpsSerial.read());
  } while (millis() - start < ms);
}



// void printWifiStatus() {
// /* -------------------------------------------------------------------------- */  
//   // print the SSID of the network you're attached to:
//   Serial.print("SSID: ");
//   Serial.println(WiFi.SSID());

//   // print your board's IP address:
//   IPAddress ip = WiFi.localIP();
//   Serial.print("IP Address: ");
//   Serial.println(ip);

//   // print the received signal strength:
//   long rssi = WiFi.RSSI();
//   Serial.print("signal strength (RSSI):");
//   Serial.print(rssi);
//   Serial.println(" dBm");
// }