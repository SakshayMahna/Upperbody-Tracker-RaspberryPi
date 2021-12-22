from threading import Thread, Lock, Event
import time
from datetime import datetime
import pigpio

time_cycle = 80

class ThreadPublisher(Thread):
    def __init__(self, publisher, kill_event):
        self.publisher = publisher
        self.kill_event = kill_event
        Thread.__init__(self, args = kill_event)

    def run(self):
        while not self.kill_event.is_set():
            start_time = datetime.now()
            self.publisher.publish()
            finish_time = datetime.now()

            dt = finish_time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0

            if ms < time_cycle:
                time.sleep((time_cycle - ms) / 1000.0)

class Motor:
    def __init__(self):
        self.current_angle = 90
        self.pi = pigpio.pi()
        self.pi.set_mode(4, pigpio.OUTPUT)
        self.pi.set_servo_pulsewidth(4, 1500)

        self.lock = Lock()
        self.kill_event = Event()
        self.thread = ThreadPublisher(self, self.kill_event)

        self.thread.daemon = True
        self.start()

    def publish(self):
        self.lock.acquire()
        signal = self.data
        self.lock.release()
        self.pi.set_servo_pulsewidth(4, signal)

    def stop(self):
        self.kill_event.set()

    def start(self):
        self.kill_event.clear()

    def send_command(self, signal):
        self.lock.acquire()
        self.data = signal
        self.lock.release()