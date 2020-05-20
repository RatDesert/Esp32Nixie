from machine import Pin, PWM, I2C, RTC
import time
import gc
import array
from utils import list_shuffle

class Lamps:
    __slots__ = ()
    #initial setup

    #PWM class object that can be needed in case of off function HV_PWM.deinit()
    HV_PWM = None

    #Built-in RTC
    _RTC = RTC()

    #K155 pins
    X0 = Pin(32, Pin.OUT)
    X1 = Pin(33, Pin.OUT)
    X2 = Pin(19, Pin.OUT)
    X3 = Pin(23, Pin.OUT)

    #IN14 pins
    L0_H1 = Pin(4, Pin.OUT)
    L1_H0 = Pin(5, Pin.OUT)
    L2_M1 = Pin(15, Pin.OUT)
    L3_M0 = Pin(12, Pin.OUT)
    L4_S1 = Pin(13, Pin.OUT)
    L5_S0 = Pin(26, Pin.OUT)

        #Init with all lamp on
    L0_H1.value(1)
    L1_H0.value(1)
    L2_M1.value(1)
    L3_M0.value(1)
    L4_S1.value(1)
    L5_S0.value(1)

    
    # Decryptor bit set -> number
    numbers = {0: 0b1000, 1: 0b0000, 2: 0b1001, 3: 0b0001, 4: 0b1110, 5: 0b0110, 6: 0b1010, 7: 0b0010, 8: 0b1100, 9: 0b0100}
    lamps = (L0_H1, L1_H0, L2_M1, L3_M0, L4_S1, L5_S0)
    time_now = [0] * 6

    #Init decryptor value -> 0b1000 -> 0
    X0.value(1)
    X1.value(0)
    X2.value(0)
    X3.value(0)
    
    @classmethod
    def _set_number(cls, number):

        flag = cls.numbers[number]
        cls.X0.value(flag >> 3 & 1)
        cls.X1.value(flag >> 2 & 1)
        cls.X2.value(flag >> 1 & 1)
        cls.X3.value(flag >> 0 & 1)
       
    @classmethod
    #set date from DS1307, should call after setup with WEB time
    def set_date(cls):
        i2c = I2C(scl=Pin(22), sda=Pin(21), freq=32768)
        ds = DS1307(i2c)
        time_now = ds.datetime()
        cls._RTC.init(time_now)

    @classmethod
    def on(cls):
        if not cls.L0_H1.value():
            raise AssertionError
        cls.HV_PWM = PWM(Pin(18), freq=20000, duty=850)

    @classmethod
    def off(cls):
        cls.HV_PWM.deinit()
    

    @classmethod
    def _scrolling_numbers(cls, time_now):
        
        for z in range(60):
            # timer = 50 + (z ** (z / 60) / 3)
            timer = (2.7 ** (z/50)) * 10
            number_list = list(range(10))
            list_shuffle(number_list)
            if z >= 10:
                number_list[0:(z // 10)] = time_now[0:(z // 10)]

            maped_time = lambda number_list: zip(cls.lamps, number_list)
            start_time = time.ticks_ms()

            while time.ticks_diff(time.ticks_ms(), start_time) <= timer:
                
                for lamp, number in maped_time(number_list):

                    cls._set_number(number)
                    lamp.value(1)
                    start = time.ticks_us()
                    gc.collect()
                    diff = time.ticks_diff(time.ticks_us(), start)

                    time.sleep_us(2000 - diff)
                    lamp.value(0)
                    time.sleep_us(1100)
                        
    @classmethod
    def _time_now(cls):

        time_now = cls.time_now
        for n, number in enumerate(cls._RTC.datetime()[4:-1]):
            time_now[2 * n], time_now[2 * n + 1] = number // 10, number % 10
        return time_now

    @classmethod 
    def show_time(cls, scrolling=True):
        time_now = cls._time_now()
        #time_now[3:] == (0, 0, 0) for 10 min
        #time_now[5] for 10 sec
        if  tuple(time_now[4:]) == (0, 0) and scrolling:
            print('here')
            cls._scrolling_numbers(time_now)
            time_now = cls._time_now()

        maped_time = zip(cls.lamps, time_now)

        for lamp, number in maped_time:

            cls._set_number(number)
            lamp.value(1)
            start = time.ticks_us()
            gc.collect()
            diff = time.ticks_diff(time.ticks_us(), start)

            time.sleep_us(2000 - diff)
            lamp.value(0)
            time.sleep_us(1100)

from micropython import const

DATETIME_REG = const(0) # 0x00-0x06
CHIP_HALT    = const(128)
CONTROL_REG  = const(7) # 0x07
RAM_REG      = const(8) # 0x08-0x3F

class DS1307(object):
    """Driver for the DS1307 RTC."""
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.weekday_start = 1
        self._halt = False

    def _dec2bcd(self, value):
        """Convert decimal to binary coded decimal (BCD) format"""
        return (value // 10) << 4 | (value % 10)

    def _bcd2dec(self, value):
        """Convert binary coded decimal (BCD) format to decimal"""
        return ((value >> 4) * 10) + (value & 0x0F)

    def datetime(self, datetime=None):
        """Get or set datetime"""
        if datetime is None:
            buf = self.i2c.readfrom_mem(self.addr, DATETIME_REG, 7)
            return (
                self._bcd2dec(buf[6]) + 2000, # year
                self._bcd2dec(buf[5]), # month
                self._bcd2dec(buf[4]), # day
                self._bcd2dec(buf[3] - self.weekday_start), # weekday
                self._bcd2dec(buf[2]), # hour
                self._bcd2dec(buf[1]), # minute
                self._bcd2dec(buf[0] & 0x7F), # second
                0 # subseconds
            )
        buf = bytearray(7)
        buf[0] = self._dec2bcd(datetime[6]) & 0x7F # second, msb = CH, 1=halt, 0=go
        buf[1] = self._dec2bcd(datetime[5]) # minute
        buf[2] = self._dec2bcd(datetime[4]) # hour
        buf[3] = self._dec2bcd(datetime[3] + self.weekday_start) # weekday
        buf[4] = self._dec2bcd(datetime[2]) # day
        buf[5] = self._dec2bcd(datetime[1]) # month
        buf[6] = self._dec2bcd(datetime[0] - 2000) # year
        if (self._halt):
            buf[0] |= (1 << 7)
        self.i2c.writeto_mem(self.addr, DATETIME_REG, buf)

    def halt(self, val=None):
        """Power up, power down or check status"""
        if val is None:
            return self._halt
        reg = self.i2c.readfrom_mem(self.addr, DATETIME_REG, 1)[0]
        if val:
            reg |= CHIP_HALT
        else:
            reg &= ~CHIP_HALT
        self._halt = bool(val)
        self.i2c.writeto_mem(self.addr, DATETIME_REG, bytearray([reg]))

    def square_wave(self, sqw=0, out=0):
        """Output square wave on pin SQ at 1Hz, 4.096kHz, 8.192kHz or 32.768kHz,
        or disable the oscillator and output logic level high/low."""
        rs0 = 1 if sqw == 4 or sqw == 32 else 0
        rs1 = 1 if sqw == 8 or sqw == 32 else 0
        out = 1 if out > 0 else 0
        sqw = 1 if sqw > 0 else 0
        reg = rs0 | rs1 << 1 | sqw << 4 | out << 7
        self.i2c.writeto_mem(self.addr, CONTROL_REG, bytearray([reg]))

from neopixel import NeoPixel

class Led:
    __slots__ = ()

    LED = NeoPixel(Pin(25, Pin.OUT), 6)

    @classmethod
    def change_color(cls, rgb):
        LED = cls.LED
        for x in range(6):
            LED[x] = rgb
            LED.write()


