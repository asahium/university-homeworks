// 122071555 = 5086314 × 24 + 19
#pragma config(Motor,  motorB,          rightMotor,    tmotorNXT, PIDControl, driveRight, encoder)
#pragma config(Motor,  motorC,          leftMotor,     tmotorNXT, PIDControl, driveLeft, encoder)

const int ForwardSpeed = 80;
const int TurnSpeed = 30;

void driveForward(int speed, int duration);
void driveBackward(int speed, int duration);
void turnRight(int duration);
void turnLeft(int duration);
void stopRobot();

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

void turnRight(int duration) {
    setMotorSpeed(leftMotor, TurnSpeed);
    setMotorSpeed(rightMotor, -TurnSpeed);
    sleep(duration);
}

void turnLeft(int duration) {
    setMotorSpeed(leftMotor, -TurnSpeed);
    setMotorSpeed(rightMotor, TurnSpeed);
    sleep(duration);
}

void stopRobot() {
    setMotorSpeed(leftMotor, 0);
    setMotorSpeed(rightMotor, 0);
}

task main()
{
    turnLeft(1085);
    driveForward(ForwardSpeed, 5500);
    turnRight(1130);
    driveForward(ForwardSpeed, 6000);
    turnRight(1100);
    driveForward(ForwardSpeed, 2300);
    turnLeft(1000);
    driveForward(ForwardSpeed, 3000);
    turnRight(880);
    driveForward(ForwardSpeed, 2100);
    turnRight(900);
    driveForward(ForwardSpeed, 1400);
    turnLeft(750);
    driveForward(ForwardSpeed, 2400);
    turnLeft(980);
    driveForward(ForwardSpeed, 2600);
    driveBackward(ForwardSpeed, 2600);
    turnRight(880);
    driveForward(ForwardSpeed, 3000);
    turnLeft(765);
    driveForward(ForwardSpeed, 1000);
    stopRobot();
}
