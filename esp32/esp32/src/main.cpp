#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <SPIFFS.h>
#include <driver/i2s.h>

#define I2S_WS  25  // LRCK
#define I2S_SD  33  // DOUT from MAX9814
#define I2S_SCK 26

#define SAMPLE_RATE     16000
#define SAMPLE_BITS     I2S_BITS_PER_SAMPLE_16BIT
#define BUFFER_SIZE     1024
#define THRESHOLD       10  
#define MAX_RECORD_DURATION_MS 10000 
const char* ssid = "Nirosh";
const char* password = "Ab@12345";
const char* serverURL = "http://192.168.1.3:5000/upload";
unsigned long recordStartTime = 0; 

bool isRecording = false;
File audioFile;
// put function declarations here:

void setupI2S() {
  i2s_config_t i2s_config = {
    .mode = i2s_mode_t(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = SAMPLE_BITS,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S_MSB,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 1024
  };

  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD
  };

  i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pin_config);
}
void sendToServer(const char* filename) {
  File file = SPIFFS.open(filename);
  if (!file || file.isDirectory()) {
    Serial.println("Failed to open file for sending");
    return;
  }

  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/octet-stream");

  int httpResponseCode = http.sendRequest("POST", &file, file.size());
  Serial.printf("Upload finished with code: %d\n", httpResponseCode);
  
  http.end();
  file.close();

  if (httpResponseCode == 200) {
    if (SPIFFS.remove(filename)) {
      Serial.println("Recording deleted from ESP32");
    } else {
      Serial.println("Failed to delete recording from ESP32");
    }
  }
}


void setup() {
 Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("WiFi connected");

  if (!SPIFFS.begin(true)) {
    Serial.println("SPIFFS Mount Failed");
    return;
  }

  setupI2S();
}

void loop() {
  uint8_t buffer[BUFFER_SIZE];
  size_t bytesRead;

  i2s_read(I2S_NUM_0, &buffer, BUFFER_SIZE, &bytesRead, portMAX_DELAY);

  int16_t* samples = (int16_t*)buffer;
  int samplesCount = bytesRead / 2;
  long sum = 0;

  for (int i = 0; i < samplesCount; i++) {
    sum += abs(samples[i]);
  }
  int average = sum / samplesCount;

  Serial.printf("Volume: %d\n", average);

  // Start recording if above threshold and not already recording
  if (average > THRESHOLD && !isRecording) {
    Serial.println("Sound detected. Start recording...");
    audioFile = SPIFFS.open("/recording.raw", FILE_WRITE);
    isRecording = true;
    recordStartTime = millis();
  }

  if (isRecording) {
    audioFile.write(buffer, bytesRead);

    // Stop only if both: volume is low AND time exceeded
    bool belowThreshold = average < (THRESHOLD / 2);  // hysteresis
    bool durationExceeded = millis() - recordStartTime > MAX_RECORD_DURATION_MS;

    if (belowThreshold && durationExceeded) {
      Serial.println("Stopping recording...");
      audioFile.close();
      isRecording = false;
      sendToServer("/recording.raw");
    }
  }

  delay(50);
}


