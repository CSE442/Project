// ***********Variables***********
int RLPower, UDPower, decodedUD, decodedRL, intInput;
int currentRightMotorSpeed, currentLeftMotorSpeed, lastRightMotorSpeed, lastLeftMotorSpeed;
boolean boolUpDown, boolRightLeft;
  // boolupDown = true == Up == 0
  // boolupDown = false == Backward == 1
  // boolRightLeft = true == Right == 0
  // boolRightLeft = false == Left == 1

// ***********I/O Pins***********
const int leftMotorDirection = 12, rightMotorDirection = 13;
const int leftMotorSpeed = 3, rightMotorSpeed = 11;
const int leftMotorBrake = 9, rightMotorBrake = 8;

// ***********Functions***********
void ReadByte(){
  byte byteInput;
  while(Serial.available()<0){
    delay(20);
  }
  byteInput = Serial.read();
  intInput = (byte) byteInput;
}
void DecodeByte(){  
  //Up/Down bit
  if( intInput >= 128 ) { // left most Bit == 1
    boolUpDown = false;
    intInput = intInput-128;
  }
  else 
    boolUpDown = true; // left most bit == 0
    
  //Left/Right bit
  if( intInput >=64 ) {// 2nd Left Most Bit == 1
    boolRightLeft = false;
    intInput = intInput-64;
  }
  else
    boolRightLeft = true; // 2nd left most bit = 0

  // Up/Down Power Bits
  if( intInput >=32) {// 3rd Left Most Bit
    UDPower = 4;
    intInput = intInput-32;
  }
  if( intInput >=16) {// 4th Left Most Bit
    UDPower = UDPower + 2;
    intInput = intInput-16;
  }
  if( intInput >=8) {// 5th Left Most Bit
    UDPower = UDPower + 1;
    intInput = intInput-8;
  }
  // Left/Right Power Bits
  if( intInput >=4) {// 3rd Right Most Bit
    RLPower = 4;
    intInput = intInput-4;
  }
  if( intInput >=2) {// 2nd Right Most Bit
    RLPower = RLPower + 2;
    intInput = intInput-2;
  }
  if( intInput >=1) {// Right Most Bit
    RLPower = RLPower + 1;
    intInput = intInput-1;
  }
  if(boolUpDown == false)
    UDPower = UDPower * -1;
  if(boolRightLeft == false)
    RLPower = RLPower * -1;
}

void CalculateMotorSpeeds(){
  int tempMotorSpeed;
  if(decodedUD == 0){
    currentLeftMotorSpeed = decodedUD;
    currentRightMotorSpeed = -1 *decodedRL;
  }
  else if(decodedRL == 0){
    currentLeftMotorSpeed = decodedUD;
    currentRightMotorSpeed = decodedRL;
  }
  else{
    currentLeftMotorSpeed = decodedUD;
    currentRightMotorSpeed = decodedUD - decodedRL;
  }
  // Handling cases besides Up, Right
  if(boolUpDown == false){ // Backwards, Negate
    currentLeftMotorSpeed = -1*currentLeftMotorSpeed;
    currentRightMotorSpeed = -1*currentRightMotorSpeed;
  }
  if(boolUpDown == false) {// Left, Switch Motors
    tempMotorSpeed = currentLeftMotorSpeed;
    currentLeftMotorSpeed = currentRightMotorSpeed;
    currentRightMotorSpeed = tempMotorSpeed;
  }
}

void SetMotorSpeeds(){
  if(currentLeftMotorSpeed > lastLeftMotorSpeed)
    currentLeftMotorSpeed = lastLeftMotorSpeed + 1;
  else if(currentLeftMotorSpeed < lastLeftMotorSpeed)
    currentLeftMotorSpeed = lastLeftMotorSpeed - 1;
    
  if(currentRightMotorSpeed > lastRightMotorSpeed)
    currentRightMotorSpeed = lastRightMotorSpeed + 1;
  else if(currentRightMotorSpeed < lastRightMotorSpeed)
    currentRightMotorSpeed = lastRightMotorSpeed - 1;

  if(currentRightMotorSpeed == 0){
    digitalWrite(rightMotorSpeed, 0);
    digitalWrite(rightMotorBrake, HIGH);
  }
  else{
    digitalWrite(rightMotorBrake, LOW);
    if(currentRightMotorSpeed < 0){
      digitalWrite(rightMotorDirection, LOW);
      digitalWrite(rightMotorSpeed, currentRightMotorSpeed *(255/7));
    }
    else if(currentRightMotorSpeed < 0){
      digitalWrite(rightMotorDirection, HIGH);
      digitalWrite(rightMotorSpeed, currentRightMotorSpeed *(255/7));
    }
  }  
  if(currentLeftMotorSpeed == 0){
    digitalWrite(leftMotorSpeed, 0);
    digitalWrite(leftMotorBrake, HIGH);
  }
  else{
    digitalWrite(leftMotorBrake, LOW);
    if(currentLeftMotorSpeed < 0){
      digitalWrite(leftMotorDirection, LOW);
      digitalWrite(leftMotorSpeed, currentLeftMotorSpeed *(255/7));
    }
    else if(currentLeftMotorSpeed < 0){
      digitalWrite(leftMotorDirection, HIGH);
      digitalWrite(leftMotorSpeed, currentLeftMotorSpeed *(255/7));
    }
  }  
  lastRightMotorSpeed = currentRightMotorSpeed;
  lastLeftMotorSpeed = currentLeftMotorSpeed;
}

// ***********Main:***********
void setup() {
  Serial.begin(9600);
  //TODO: Set Pins 
}
void loop() {
  ReadByte();
  DecodeByte();
  CalculateMotorSpeeds();
  SetMotorSpeeds();
  delay(100);
}