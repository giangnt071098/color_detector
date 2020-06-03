class TCS3200
{
  private:
    int PW;
  
    int redMin = 45;  // Do cac gia tri Min max ban dau
    int redMax = 220;  // cua 3 mau de map gia tri 0->255 tuong ung 
    int greenMin = 47; // voi min -> max
    int greenMax = 248; 
    int blueMin = 38; 
    int blueMax =172; 
  public:
    byte S2,S3;
    int sensorout;
    TCS3200(byte S2, byte S3, int sensorout)
    {
      this->S2 = S2;
      this->S3 = S3;
      this->sensorout = sensorout;
    }
    int getredvalue()
    {
      digitalWrite(S2, LOW);
      digitalWrite(S3, LOW);
      PW = pulseIn(sensorout, LOW);
      return PW;
    }
    int getgreenvalue()
    {
      digitalWrite(S2, HIGH);
      digitalWrite(S3, HIGH);
      PW = pulseIn(sensorout, LOW);    
      return PW;
    }
    int getbluevalue()
    {
      digitalWrite(S2, LOW);
      digitalWrite(S3, HIGH);
      PW = pulseIn(sensorout, LOW);
      return PW;
    }
    int norm(int value)
    {
      if (value > 255)
        return 255;
      else if (value < 0 )
        return 0;
      else 
        return value;
    }

    void display(int red, int green, int blue, bool check)
    {
      if (!check)
        {
          red = norm(map(red, redMin, redMax, 255, 0));
          green = norm(map(green, greenMin, greenMax, 255, 0));
          blue = norm(map(blue, blueMin, blueMax, 255, 0));
        }
      Serial.print("Red = ");
      Serial.print(red);
      Serial.print(" - Green = ");
      Serial.print(green);
      Serial.print(" - Blue = ");
      Serial.println(blue);
    } 
  };
