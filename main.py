from flask import Flask, Response
import cv2
import time

app = Flask(__name__)
camera = cv2.VideoCapture(0)


def gen_frames():
    while True:
        print(time.time())
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    return """
<body>
<div class="container">
    <div class="row">
        <div class="col-lg-8 offset-lg-2">
            <h3 class="mt-5">Live Streaming</h3>
            <img src="/video_feed" style="object-fit: contain; width: 100%; height: 100%">
        </div>
    </div>
</div>
</body>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
