# IoT
CM3603 - A responsive web application for tracking train information, schedules, and alerts in Sri Lanka.

## Features

- Real-time train alerts by line
- Train schedules
- Responsive design for all devices

## Technologies Used

- React
- TypeScript
- Tailwind CSS
- React Router
- Lucide React Icons

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/nisal2002/IoT.git
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:5173](http://localhost:5173) in your browser.

## Project Structure

```
src/
├── components/
│   ├── LoadingScreen.tsx
│   ├── MainPage.tsx
│   ├── LiveTrainAlerts.tsx
│   └── MainLineAlerts.tsx
├── App.tsx
└── main.tsx
```


## Sinhala Speech to Text Converter

This project is a simple Python application that:

1. Records Sinhala speech via a microphone.
2. Converts recorded audio to Sinhala Unicode text using Google Speech Recognition.
3. Optionally converts Sinhala Unicode text to Singlish using an external API.

---

## Features

- Record audio in real-time from your microphone.
- Automatic speech recognition (ASR) for Sinhala using Google’s Speech API.
- Convert recognized Sinhala text into Singlish.
- User-friendly terminal prompts and repeat recording capability.

---

## Requirements

- Python 3.7 or higher
- Microphone input enabled
- Internet connection (for Google Speech Recognition and Singlish API)

---
