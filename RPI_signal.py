import RPi.GPIO as GPIO
from board import SCL, SDA
import busio

# Import the SSD1306 module.
import adafruit_ssd1306

from PIL import Image, ImageDraw, ImageFont

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

BORDER = 0

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

image = Image.new("1", (display.width, display.height))

display.fill(0)

draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)

font = ImageFont.load_default()


def beep(on):
    if on:
        GPIO.output(23, GPIO.HIGH)
    else:
        GPIO.output(23, GPIO.LOW)


def led(on):
    if on:
        GPIO.output(24, GPIO.HIGH)
    else:
        GPIO.output(24, GPIO.LOW)


def print_book(isbn, title):
    x = 0
    padding = 2
    top = padding

    draw.text((x, top + 0), title, font=font, fill=255)
    draw.text((x, top + 16), isbn, font=font, fill=255)

    # Display image
    display.image(image)
    display.show()
