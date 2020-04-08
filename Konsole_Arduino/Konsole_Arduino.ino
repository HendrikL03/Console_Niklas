#define PIN_RED1 3
#define PIN_GRN1 2
#define PIN_BLU1 4
#define PIN_RED2 6
#define PIN_GRN2 5
#define PIN_BLU2 7
#define PIN_WW 11
#define PIN_WK 12

#define PIN_RGB_RLS1 40 // Relais 2
#define PIN_RGB_RLS2 42 // Relais 3
#define PIN_RGB_RLS3 44 // Relais 4
#define PIN_WK_RLS1 46 // Relais 5
#define PIN_WK_RLS2 48 // Relais 6
#define PIN_RLLD_UP 50 // Relais 7
#define PIN_RLLD_DOWN 52 // Relais 8


int pin_array[] = {
    PIN_RED1, 
    PIN_GRN1, 
    PIN_BLU1, 
    PIN_RED2, 
    PIN_GRN2, 
    PIN_BLU2, 
    PIN_WW, 
    PIN_WK, 
    PIN_RGB_RLS1, 
    PIN_RGB_RLS2, 
    PIN_RGB_RLS3, 
    PIN_WK_RLS1, 
    PIN_WK_RLS2,  
    PIN_RLLD_UP, 
    PIN_RLLD_DOWN
};


void setup() {
    Serial.begin(115200);

    // Setup Pins
    for (int i=0; i < 8; i++) {
        pinMode(pin_array[i], OUTPUT);
        digitalWrite(pin_array[i], LOW);
    }
    for (int i=8; i < 15; i++) {
        pinMode(pin_array[i], OUTPUT);
        digitalWrite(pin_array[i], HIGH);
    }
    
    while (Serial.available()) {Serial.read();}
    
}

uint16_t header;
byte data;    

void loop() {
    if (Serial.available() > 1){
        // header lesen
        header = (Serial.read() << 8) + Serial.read();
        
        // Durch Header iterieren und wenn Bit 1 ist, Wert lesen und setzen
        for (int i = 0; i < 15; i++) {
            if ((header & 0x8000 >> i) != 0) {
                while (!Serial.available()) {}
                data = Serial.read();
                analogWrite(pin_array[i], data);
            }
        }
    }

}
