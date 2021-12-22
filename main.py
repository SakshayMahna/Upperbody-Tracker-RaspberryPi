from camera import CameraThread
from detector import HaarCascadeDetector
from motor import Motor, ThreadPublisher
from threading import Event
import cv2

width = 320
height = 240

if __name__ == "__main__":
    kill_event = Event()
    cam = CameraThread(kill_event, height = height, width = width)
    cam.start()

    detector = HaarCascadeDetector("haarcascade_upperbody.xml")
    motor = Motor()

    threshold = 8
    rate = 2
    mid_x = width // 2

    while True:
        frame = cam.read()
        try:
            x, y, w, h = detector.detect(frame)
            frame = cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            mid_x = int((x + x + w) // 2)
        except TypeError:
            pass

        if abs(mid_x - width // 2) > threshold:
            if mid_x > width // 2:
                motor.current_angle += rate
            if mid_x < width // 2:
                motor.current_angle -= rate
            
            signal = 1000 * (1 + motor.current_angle / 180)
            motor.send_command(signal)

        cv2.imshow('webcam', frame)
        if cv2.waitKey(1) == 27:
            break

    kill_event.set()
    motor.stop()
    cv2.destroyAllWindows()
