import micropython
import array
import time

REG_W1TS_0_31 = 0x3FF44008
REG_W1TS_32_39 = 0x3FF44014


@micropython.viper
def test(pin: int, bit):
    ptr = ptr32(0x3FF44004)
    state = ptr[0]

    mask = 1 << pin
    state = int(state)

    state ^= (int(-bit) ^ state) & (1 << pin)

    ptr[0] = state

def comp_array():
    a = array.array('B', [2, 3, 4, 3, 1, 1])
    l = [2, 3, 4, 3, 1, 1]

    start_time = time.ticks_us()
    for i in range(6):
        k = a[i]
    print(time.ticks_diff(time.ticks_us(), start_time))

    start_time = time.ticks_us()
    for i in range(6):
        k = l[i]
    print(time.ticks_diff(time.ticks_us(), start_time))