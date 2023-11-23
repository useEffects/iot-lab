int ldrPin = A0;

void setup() {
   // put your setup code here, to run once:
    pinMode(13,OUTPUT);
    Serial.begin(9600);
}
void loop() {
   // put your main code here, to run repeatedly:

   int val = analogRead(ldrPin);
   if(val > 490) {
    Serial.println("Dark");
    digitalWrite(13,HIGH);
   }
   else{
   Serial.println("Brigth");
   digitalWrite(13,LOW);
   }
   delay(1000);
}
