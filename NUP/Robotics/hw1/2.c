// 122071555 = 5086314 × 24 + 19
#pragma config(Sensor, S2,     gyroSensor,     sensorEV3_Gyro)
#pragma config(Motor,  motorB,          rightMotor,    tmotorEV3_Large, PIDControl, driveRight, encoder)
#pragma config(Motor,  motorC,          leftMotor,     tmotorEV3_Large, PIDControl, driveLeft, encoder)

const int ForwardSpeed = 80;
const int TurnSpeed = 20;
const int TurnAngle = 84;

void driveForward(int speed, int duration);
void driveBackward(int speed, int duration);
void rotateRight(int angle);
void rotateLeft(int angle);
void stopMotors();

void driveForward(int speed, int duration) {
    setMotorSpeed(leftMotor, speed);
    setMotorSpeed(rightMotor, speed);
    sleep(duration);
}

void driveBackward(int speed, int duration) {
    setMotorSpeed(leftMotor, -speed);
    setMotorSpeed(rightMotor, -speed);
    sleep(duration);
}

void rotateRight(int angle) {
    resetGyro(gyroSensor);
    while(getGyroDegrees(gyroSensor) < angle) {
        setMotorSpeed(leftMotor, TURN_SPEED);
        setMotorSpeed(rightMotor, -TURN_SPEED);
    }
    stopMotors();
}

void rotateLeft(int angle) {
    resetGyro(gyroSensor);
    while(getGyroDegrees(gyroSensor) > -angle)
    {
        setMotorSpeed(leftMotor, -TURN_SPEED);
        setMotorSpeed(rightMotor, TURN_SPEED);
    }
    stopMotors();
}

void stopMotors() {
    setMotorSpeed(leftMotor, 0);
    setMotorSpeed(rightMotor, 0);
}

task main() {
    rotateLeft(TurnAngle);
    driveForward(ForwardSpeed, 4700);
    rotateRight(TurnAngle);
    driveForward(ForwardSpeed, 5200);
    rotateRight(TurnAngle);
    driveForward(ForwardSpeed, 2100);
    rotateLeft(TurnAngle);
    driveForward(ForwardSpeed, 2800);
    rotateRight(TurnAngle);
    driveForward(ForwardSpeed, 1900);
    rotateRight(TurnAngle);
    driveForward(ForwardSpeed, 1100);
    rotateLeft(TurnAngle);
    driveForward(ForwardSpeed, 3000);
    rotateLeft(TurnAngle);
    driveForward(ForwardSpeed, 2200);
    driveBackward(ForwardSpeed, 2200);
    rotateRight(TurnAngle);
    driveForward(ForwardSpeed, 2600);
    rotateLeft(TurnAngle);
    driveForward(ForwardSpeed, 1000);
    stopMotors();
}
