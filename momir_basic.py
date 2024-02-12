from escpos.printer import Serial
import os, random
import RPi.GPIO as GPIO
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306 #imports of different modules
from luma.core.legacy import text
from fonts.ttf import FredokaOne
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time

BUTTON_1_PIN = 11 #Button pins 
BUTTON_2_PIN = 13
BUTTON_3_PIN = 15

cmc = 0 #cmc variable for tracking cmc

p = Serial(devfile='/dev/serial0', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1.00, dsrdtr=True) #initilize thermal printer serial 

serial = i2c(port=1, address=0x3C) #initilize OLED screen serial ports

device = ssd1306(serial) #initilize OLED screen serial communication

font16 = ImageFont.truetype(FredokaOne, 16) #set font and size for screen

def display_cmc(cmc): #function to display cmc on screen
    with canvas(device) as draw:
        draw.text((5, 30), "Current CMC: " + str(cmc), fill="white", font=font16)

display_cmc(cmc) #display initial cmc = 0

def display_print_message(cmc): #function to display print message
    with canvas(device) as draw:
        draw.text((5, 0), "Printing", fill="white", font=font16)
        draw.text((5, 30), "Current CMC: " + str(cmc), fill="white", font=font16)

GPIO.setwarnings(False) #ignore button warnings
GPIO.setmode(GPIO.BOARD)  # Set pin numbering mode to BOARD
GPIO.setup(BUTTON_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #set GPIO settings for buttons
GPIO.setup(BUTTON_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def print_random_image(cmc): #function to print image
    path = '/home/pi/momir_basic/' + str(cmc) + '/'
    image_path = path + random.choice(os.listdir(path))
    p.image(image_path)
    p.textln("")
    p.textln("")
    p.textln("")

#print_random_image(0)

debounce_delay = 0.2  # Adjust this value as needed for your buttons

while True: # Run forever
    if GPIO.input(BUTTON_1_PIN) == GPIO.LOW: #increase CMC button
        if cmc < 16: #highest cmc is 16, so we don't want to go over that
            cmc = cmc + 1
            display_cmc(cmc)
            time.sleep(debounce_delay)  # Debounce delay
        else:
            pass
    if GPIO.input(BUTTON_2_PIN) == GPIO.LOW: #decrese CMC button
        if cmc > 0: #lowest cmc is 0 so we don't want to go negative
            cmc = cmc - 1
            display_cmc(cmc)
            time.sleep(debounce_delay)  # Debounce delay
        else:
            pass
    if GPIO.input(BUTTON_3_PIN) == GPIO.LOW: #printing button
        if cmc == 14: #there are currently no CMC 14 creatures, so skip if you try printing this
            pass
        else:
            display_print_message(cmc)
            print_random_image(cmc)
            time.sleep(debounce_delay)  # Debounce delay
