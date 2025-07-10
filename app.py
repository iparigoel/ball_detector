from flask import Flask, render_template, Response
from flask_sock import Sock
import cv2
import numpy as np
import threading
import time

app = Flask(__name__)
sock = Sock(app)

video = cv2.VideoCapture(0)

latest_data = {'x': 0, 'y': 0, 'r': 0}

def dist(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2

def generate_frames():
    global latest_data
    prevCircle = None

    while True:
        ret, frame = video.read()
        if not ret:
            continue  # skip frame

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (19, 19), 0)
        circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.2, 100,
                                   param1=140, param2=50, minRadius=60, maxRadius=400)

        center_x, center_y, radius = 0, 0, 0

        if circles is not None:
            circles = np.uint16(np.around(circles))
            chosen = None
            for i in circles[0, :]:
                if chosen is None:
                    chosen = i
                elif prevCircle is not None and dist(i[0], i[1], prevCircle[0], prevCircle[1]) < dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]):
                    chosen = i

            if chosen is not None:
                center_x, center_y, radius = chosen[0], chosen[1], chosen[2]
                cv2.circle(frame, (center_x, center_y), 1, (0, 255, 0), 3)
                cv2.circle(frame, (center_x, center_y), radius, (255, 0, 0), 3)
                prevCircle = chosen

        latest_data = {'x': int(center_x), 'y': int(center_y), 'r': int(radius)}

        cv2.putText(frame, f"({center_x}, {center_y}) r={radius}", (center_x + 10, center_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@sock.route('/ws')
def websocket(ws):
    while True:
        time.sleep(0.2)
        ws.send(str(latest_data))  # sent as string; frontend parses it

if __name__ == '__main__':
    app.run(debug=True)
