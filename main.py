from flask import Flask
from flask_sock import Sock
import cv2
import base64
import threading
import time

app = Flask(__name__)
sock = Sock(app)

# 카메라 설정
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

clients = []

def send_frames():
    global clients
    while True:
        if len(clients) > 0:
            ret, frame = camera.read()
            if not ret:
                continue

            # 흑백 변환
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # JPEG로 인코딩
            _, buffer = cv2.imencode('.jpg', gray_frame)
            encoded_frame = base64.b64encode(buffer).decode('utf-8')

            # 모든 클라이언트에 전송
            for ws in clients:
                try:
                    ws.send(encoded_frame)
                except:
                    clients.remove(ws)

        time.sleep(0.03)

@sock.route('/video')
def video(ws):
    global clients
    clients.append(ws)
    while True:
        try:
            message = ws.receive()
            if message is None:
                break
        except:
            break
    clients.remove(ws)

@app.route("/")
def root():
    # HTML이 필요 없는 경우 간단한 JSON 응답 반환
    return {"status": "Streaming server is running"}

if __name__ == "__main__":
    thread = threading.Thread(target=send_frames, daemon=True)
    thread.start()

    app.run(host="0.0.0.0", port=5000)

