  // Funcion x1 es para mover el motor en sentido positivo
  // Funcion x2 es para volver a poner al motor en su lugar de origen
  // Funcion x3 es para retornar el promedio de las 30 mediciones del Amplificador de Corriente
  
  // for incoming serial data
  int med = 10;
  int k;
  float suma;
  int contador_motor = 0;
  const int en = 8;
  const int ms1 = 9;
  const int ms2 = 10;
  const int stp = 11;
  const int dir = 12;
  bool s = true;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(stp, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(ms1, OUTPUT);
  pinMode(ms2, OUTPUT);
  pinMode(en, OUTPUT);
}


void loop() {
  if(s){
  digitalWrite(en, LOW);
  digitalWrite(ms1, LOW);
  digitalWrite(ms2, LOW);
  digitalWrite(stp, LOW);
  digitalWrite(dir, HIGH);
  s = false; 
  }
 

  // send data only when you receive data:
  if (Serial.available() > 0) {
    

    // read the incoming byte:
    String dato = Serial.readString();

   if (dato == "x1"){
    Serial.print("x1: ");
    k = motor(med, contador_motor);
    Serial.println(k);
    contador_motor += 1;
   }
   
   else if (dato == "x2"){
    Serial.println("Funcion x2: Volviendo al origen ");
    backward_engine(med);
    contador_motor = 0;
    s = true;
   }

   else if (dato == "x3"){
    suma = 0;
    for (int i=0; i < 200; i++){    
      suma = suma + analogRead(A0);
  }
    Serial.print("x3: ");
    Serial.println(suma/200*5.0/1023.0);
   }
   
    else{
      
      // say what you got:
      Serial.print("I received: ");
      Serial.println(dato);
    }
  }
}

int motor(int mediciones, int contador){
  
  int vueltas = 900.0/mediciones; //Cantidad para el for del motor
  int wavelength;
  int base = 350; 
  wavelength = base + contador * vueltas / 2;
  
  if (contador <= mediciones and wavelength <= 800){
    if (wavelength > 350){
      for(int x = 0; x < vueltas; x++){
        digitalWrite(stp, HIGH);
        delay(10);
        digitalWrite(stp, LOW);
      }
    }
    else{
      return base;      
     } 
  }
  return wavelength;
}

bool backward_engine(int mediciones){
  int vueltas = 900.0/mediciones; //Cantidad para el for del motor
  digitalWrite(dir, LOW);
  for(int i=0; i < mediciones; i++){
    for(int x = 0; x < vueltas; x++){
      digitalWrite(stp, HIGH);
      delay(10);
      digitalWrite(stp, LOW);
    }
    delay(100);
  } 
  return true;

}

