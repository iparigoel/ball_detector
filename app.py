from flask import Flask, render_template, Response
from flask_sock import Sock
import video_stream   # import our module

app = Flask(__name__)
sock = Sock(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_response():
    return Response(
        video_stream.generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@sock.route("/ws")
def websocket(ws):
    video_stream.handle_ws(ws)


if __name__ == "__main__":
    app.run(debug=True)
