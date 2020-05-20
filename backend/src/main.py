from hardware import Tubes, set_rtc_date

    #'0b1001' const'32, 33,  19, 23'
    
if __name__ == "__main__":
    # Led.change_color((20, 0, 10))
    set_rtc_date()
    Tubes.on()
    while True:
        Tubes.show_time()