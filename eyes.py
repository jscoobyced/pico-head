from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep
import framebuf

class Eyes:
    anim = 0.2
    width=128
    height=64
    
    def __init__(self, width, height, sda, scl):
        id = 0
        sda_pin = Pin(sda)
        scl_pin = Pin(scl)
        self.width = width
        self.height = height

        with open('open.pbm', 'rb') as f:
           f.readline() # magic number
           f.readline() # creator comment
           f.readline() # dimensions
           self.opened_eyes = bytearray(f.read())

        with open('closed.pbm', 'rb') as f:
           f.readline() # magic number
           f.readline() # creator comment
           f.readline() # dimensions
           self.closed_eyes = bytearray(f.read())

        self.i2c = I2C(id=id, scl=scl_pin, sda=sda_pin)
        self.oled = SSD1306_I2C(width=self.width, height=self.height, i2c=self.i2c)
        self.oled.init_display()

    def open_eyes(self):
        fb = framebuf.FrameBuffer(self.opened_eyes, self.width, self.height, framebuf.MONO_HLSB)
        self.oled.blit(fb, 0,0)
        self.oled.show()
        
    def close_eyes(self):
        fb = framebuf.FrameBuffer(self.closed_eyes, self.width, self.height, framebuf.MONO_HLSB)
        self.oled.blit(fb, 0,0)
        self.oled.show()

    def clear(self):
        self.oled.fill(0)
        self.oled.show()

    def blink(self, count):
        for i in range(count):
            self.open_eyes()
            sleep(self.anim)
            self.close_eyes()
            sleep(self.anim)
