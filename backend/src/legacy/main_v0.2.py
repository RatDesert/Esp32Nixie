from machine import Pin, PWM, I2C, RTC
from ds1307 import DS1307
import time
import gc
import random
import array

class Lamp:
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

    @staticmethod
    def shuffle(seq):
        l = len(seq)
        for i in range(l):
            j = random.randrange(l)
            seq[i], seq[j] = seq[j], seq[i]
    
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
    def _scrolling_numbers(cls, time_now, iterations):

        for z in range(iterations):
                number_list = list(range(10))
                cls.shuffle(number_list)
                
                timer = 30 + (10 ** (z / 5)) / 650

                if z >= iterations - 6:
                    current_position = z - (iterations - 7)
                    number_list[0:current_position] = time_now[0:current_position]

                    timer = timer + current_position * 10

                maped_time = lambda number_list: zip(cls.lamps, number_list)
                start_time = time.ticks_ms()
                #30 + (10 ** (z / 12)) * 2
                #30 + (10 ** (z / 5)) / 650
                if z == iterations -1:
                    delay =  cls._RTC.datetime()[-1] // 1000
                    timer = (1000 - delay) + timer / 2

                while time.ticks_diff(time.ticks_ms(), start_time) <= timer:
                    
                    for lamp, number in maped_time(number_list):
                        if z == iterations - 1 and lamp is cls.L5_S0:
                            number = cls._RTC.datetime()[6] % 10

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
        #time_now[3:] == (0, 0, 0)
        #time_now[5]
        if  time_now[5] == 0 and scrolling:
            cls._scrolling_numbers(time_now, 25)
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
            
        

if __name__ == "__main__":
    Lamp.set_date()
    Lamp.on()
    while True:
        Lamp.show_time()