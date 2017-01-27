 //Declare pin functions on Redboard
//#define stp 11
//#define dir 12
//#define MS1 9
//#define MS2 10
//#define EN  8
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
  // put your main code here, to run repeatedly:
  if(s){
  digitalWrite(en, LOW);
  digitalWrite(ms1, LOW);
  digitalWrite(ms2, LOW);
  digitalWrite(stp, LOW);
  digitalWrite(dir, LOW);
  s = false; 
  for(int x = 0; x < 200; x++){
    digitalWrite(stp, HIGH);
    delay(10);
    digitalWrite(stp, LOW);
  }

    
  }
}
