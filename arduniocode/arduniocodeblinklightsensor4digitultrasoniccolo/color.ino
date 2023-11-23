const int S0 = 8;
const int S1 = 9;
const int S2 = 10;
const int S3 = 11;
const int OUT = 12;

// Variables to store color readings
int redValue = 0;
int greenValue = 0;
int blueValue = 0;

void setup() {
  // Initialize color sensor pins
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(OUT, INPUT);

  // Set frequency scaling to 20%
  digitalWrite(S0, HIGH);
  digitalWrite(S1, LOW);

  Serial.begin(9600);
}

void loop() {
  // Read red light
  digitalWrite(S2, LOW);
  digitalWrite(S3, LOW);
  redValue = pulseIn(OUT, LOW);

  // Read green light
  digitalWrite(S2, HIGH);
  digitalWrite(S3, HIGH);
  greenValue = pulseIn(OUT, LOW);

  // Read blue light
  digitalWrite(S2, LOW);
  digitalWrite(S3, HIGH);
  blueValue = pulseIn(OUT, LOW);

  // Print the RGB values
  Serial.print("Red: ");
  Serial.print(redValue);
  Serial.print(" Green: ");
  Serial.print(greenValue);
  Serial.print(" Blue: ");
  Serial.println(blueValue);

  delay(500);
}
