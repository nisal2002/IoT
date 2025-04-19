#include <Arduino.h>
#include "train_model.cc"  // your TFLite model array
#include "C:/CM3603/esp32/esp32-cam/lib/Chirale_TensorFlowLite/src/tensorflow/lite/micro/all_ops_resolver.h"
#include "C:/CM3603/esp32/esp32-cam/lib/Chirale_TensorFlowLite\src/tensorflow/lite/micro/micro_interpreter.h"
#include "C:\CM3603\esp32\esp32-cam\lib/Chirale_TensorFlowLite\src\tensorflow\lite\schema\schema_generated.h"
#include "C:\CM3603\esp32\esp32-cam\lib/Chirale_TensorFlowLite\src\Chirale_TensorFlowLite.h"
#include "esp_camera.h"

constexpr int tensor_arena_size = 40 * 1024;
uint8_t tensor_arena[tensor_arena_size];

tflite::MicroInterpreter* interpreter;
TfLiteTensor* input;
TfLiteTensor* output;
bool train_detected = false;

void preprocess_image_grayscale(camera_fb_t* fb, uint8_t* output, int model_width, int model_height) {
  int src_width = fb->width;
  int src_height = fb->height;
  uint8_t* src = fb->buf;

  for (int y = 0; y < model_height; y++) {
    for (int x = 0; x < model_width; x++) {
      int src_x = x * src_width / model_width;
      int src_y = y * src_height / model_height;

      int pixel_index = (src_y * src_width + src_x) * 2;  // RGB565 format
      uint16_t pixel = (src[pixel_index + 1] << 8) | src[pixel_index];

      uint8_t r = ((pixel >> 11) & 0x1F) << 3;
      uint8_t g = ((pixel >> 5) & 0x3F) << 2;
      uint8_t b = (pixel & 0x1F) << 3;

      uint8_t gray = (r * 30 + g * 59 + b * 11) / 100;
      output[y * model_width + x] = gray;
    }
  }
}

void setup() {
  Serial.begin(115200);

  // Camera config for ESP32-CAM
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = 5;
  config.pin_d1 = 18;
  config.pin_d2 = 19;
  config.pin_d3 = 21;
  config.pin_d4 = 36;
  config.pin_d5 = 39;
  config.pin_d6 = 34;
  config.pin_d7 = 35;
  config.pin_xclk = 0;
  config.pin_pclk = 22;
  config.pin_vsync = 25;
  config.pin_href = 23;
  config.pin_sscb_sda = 26;
  config.pin_sscb_scl = 27;
  config.pin_pwdn = 32;
  config.pin_reset = -1;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_RGB565;
  config.frame_size = FRAMESIZE_QVGA;
  config.fb_count = 1;

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Camera init failed");
    while (true);  // Stop execution
  }

  // Load TFLite model
  const tflite::Model* model = tflite::GetModel(model_tflite);
  static tflite::AllOpsResolver resolver;
  static tflite::MicroInterpreter static_interpreter(model, resolver, tensor_arena, tensor_arena_size);
  interpreter = &static_interpreter;

  if (interpreter->AllocateTensors() != kTfLiteOk) {
    Serial.println("Tensor allocation failed");
    while (true);
  }

  input = interpreter->input(0);
  output = interpreter->output(0);
}

void loop() {
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  // Resize and grayscale preprocess (e.g., 96x96 model input)
  preprocess_image_grayscale(fb, input->data.uint8, input->dims->data[2], input->dims->data[1]);

  // Run inference
  if (interpreter->Invoke() != kTfLiteOk) {
    Serial.println("Inference failed");
  } else {
    float prediction = output->data.f[0];
    train_detected = (prediction > 0.5);  // adjust threshold if needed
    Serial.print("Train detected: ");
    Serial.println(train_detected);
  }

  esp_camera_fb_return(fb);
  delay(200);
}