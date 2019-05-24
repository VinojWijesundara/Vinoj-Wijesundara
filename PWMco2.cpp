//program: PWMco2 

#include <iostream>  
#include <wiringPi.h>
using namespace std;

const int PWM=5;

int getPWM()
 
{ 
     //wait till PWM start
     while (digitalRead(PWM)== LOW);
     //wait till PWM end 
     long startTime = micros();
     while (digitalRead(PWM) == HIGH);
     long duration = micros() - startTime;
     //from datasheet 
     //CO2 ppm = 50000 *(Th - 2ms) / (Th + T1 - 4ms) 
     long co2ppm = 50* ((duration/1000) - 2); 
     return co2ppm;
} 
int main(void) 
{ 
     wiringPiSetup();
     pinMode(PWM, INPUT);
     cout << " CO2 Pulse Width Modulation program is running .. \n";
     while (1) 
   { 
	   cout << "\nCO2 ppm = \t"<< getPWM();
	   delay (2000); 
	   } 
      return 0; 
   }
