#include <PROGMEM_readAnything.h>

const float A = pow(2, 1.0 / 12);

struct Sound{
  unsigned int beg;
  unsigned int end;
  byte note;
};

#include "raw.h"

const int SPEAKER_PIN = A1;

void setup(){
  pinMode(SPEAKER_PIN, OUTPUT);
}
 
const int maxpoly = 5;
unsigned long poly [maxpoly][3];
int pos = 0;
int count = 0;
int start = -1;

void loop(){
  unsigned long t = micros();
  if (start == -1){
    start = t;
  }
  t -= start;

  int i = 0;
  while (true){
    if (i == count){
      break;
    }
    if (t >= poly[i][1]){
      for (int j = i + 1; j < count; j ++){
        poly[j - 1][0] = poly[j][0];
        poly[j - 1][1] = poly[j][1];
        poly[j - 1][2] = poly[j][2];
      }
      count --;
    }
    else{
      if (t >= poly[i][2]){
        poly[i][2] += poly[i][0];
        digitalWrite(SPEAKER_PIN, HIGH);
        delayMicroseconds(poly[i][0] / 160);
        digitalWrite(SPEAKER_PIN, LOW);
      }
      i ++;
    }
  }

  for (int i = pos; i < len; i ++){
    Sound snd;
    PROGMEM_readAnything (&music[i], snd);
    if (t >= snd.beg * 10000UL){
      int pi;
      float freq = 440.0 * pow(A, snd.note - 69);
      unsigned long width = 500000 / freq;
      pos ++;
      if (count == maxpoly){
        pi = 0;
      }
      else{
        pi = count;
        count ++;
      }
      poly[pi][0] = width;
      poly[pi][1] = snd.end * 10000UL;
      poly[pi][2] = t + width;
    }
    else{
      break;
    }
  }
}
