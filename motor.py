from threading import Thread, Lock, Event
import time
from datetime import datetime
import RPi.GPIO as GPIO
from time import sleep

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
    def __init__(self, pin):
        self.current_angle = 90

        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        
        self.pwm = GPIO.pwm(pin, 50)
        self.pwm.start(0)

        self.lock = Lock()
        self.kill_event = Event()
        self.thread = ThreadPublisher(self, self.kill_event)

        self.thread.daemon = True
        self.start()

    def publish(self):
        self.lock.acquire()
        signal = self.data
        self.lock.release()

        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(signal)
        sleep(1)
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(signal)


    def stop(self):
        self.kill_event.set()

    def start(self):
        self.kill_event.clear()

    def send_command(self, angle):
        self.lock.acquire()
        self.data = angle / 18 + 2
        self.lock.release()