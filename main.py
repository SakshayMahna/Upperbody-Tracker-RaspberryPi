from camera import CameraThread
from detector import HaarCascadeDetector
from threading import Event
import cv2

if __name__ == "__main__":
    kill_event = Event()
    cam = CameraThread(kill_event)
    cam.start()

    detector = HaarCascadeDetector("haarcascade_upperbody.xml")

    while True:
        frame = cam.read()
        try:
            x, y, w, h = detector.detect(frame)
            frame = cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        except TypeError:
            pass

        cv2.imshow('webcam', frame)
        if cv2.waitKey(1) == 27:
            break

    kill_event.set()
    cv2.destroyAllWindows()
