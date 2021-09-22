String val;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available())
  {
    val = Serial.readStringUntil("\n");
    
    if(val.equals("on")){
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else if(val.equals("off")){
      digitalWrite(LED_BUILTIN, LOW); 
    }
    else{
      Serial.write(10);
    }
  }
}
