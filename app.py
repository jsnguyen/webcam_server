import os
from flask import Flask, render_template, Response

# import camera driver
from camera_opencv import Camera

app = Flask(__name__)

@app.route('/')
def vid():
    """Video streaming home page."""
    return render_template('index.html')


def gen_video(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen_image(camera):
    """Single image function."""
    frame = camera.get_frame()
    return (frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_video(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image_feed')
def image_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_image(Camera()),
                    mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
