void setup() {
        Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
}

void loop() {
  if (Serial.available() > 0) {
    String dato = Serial.readString();
    if (dato == "x1"){
      Serial.print("Funcion x1: ");
    }
  }
}


