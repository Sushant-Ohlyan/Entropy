import cv2


def gen_frames():
        camera = cv2.VideoCapture(0)
        global video_flag
        video_flag=1
        while True:
            if(video_flag==2):
                break
            success, frame = camera.read()  # read the camera frame
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 