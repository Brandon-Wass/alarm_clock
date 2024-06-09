import RPi.GPIO as GPIO

class GPIOHandler:
    def __init__(self, pin):
        self.gpio_pin = pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.output(self.gpio_pin, GPIO.LOW)

    def change_gpio_pin(self, gpio_pin):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        self.gpio_pin = gpio_pin
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.output(self.gpio_pin, GPIO.LOW)

    def activate_pin(self):
        GPIO.output(self.gpio_pin, GPIO.HIGH)

    def deactivate_pin(self):
        GPIO.output(self.gpio_pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()
