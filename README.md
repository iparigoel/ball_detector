# Real-Time Circular Object Detection with OpenCV, Flask, and WebSockets

This project demonstrates real-time circular object detection using OpenCV, served through a Flask backend, and enhanced with WebSockets for live data updates in the browser.

## 🚀 Features

📷 Captures frames from your webcam.

🟢 Detects circles using OpenCV’s Hough Circle Transform.

🌐 Streams the processed video feed to the browser.

⚡ Sends circle coordinates (x, y) and radius r in real time via WebSocket.

## 📂 Project Structure
ball_detector/
│
├── app.py                # Flask app entry point
├── video_stream.py       # Circle detection logic with OpenCV
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Frontend for live video + detection data

## 🛠️ Installation

Clone the repository:

git clone https://github.com/iparigoel/ball_detector.git

cd ball_detector

Install dependencies:

pip install -r requirements.txt

## ▶️ Usage

Start the Flask server:
python app.py

Open your browser and navigate to:
👉 http://127.0.0.1:5000/

You’ll see:

✅ A live webcam feed with detected circles drawn in real time.
✅ Continuously updating values of Center X, Center Y, and Radius below the video.

## 📜 License

This project is licensed under the MIT License.
