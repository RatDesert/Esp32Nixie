import time
import network

class Wifi:
    station = network.WLAN(network.STA_IF)
    access_point = network.WLAN(network.AP_IF)
    


    @classmethod
    def set_ap_conf(cls ,essid, password):
        cls.access_point.config(essid=essid, password=password, authmode=3)


    @classmethod
    def scann(cls):
        result = [{'essid': x[0].decode(),'rssi':x[3] ,'security':x[4]} for x in cls.station.scan()]
        return result

    @classmethod
    def connect(cls, essid, password):
        cls.station.connect(essid, password)
        time_start = time.time()

        while time.time() - time_start < 5:
            if cls.station.isconnected():
                return True
                

        cls.station.disconnect()
        return False

    @classmethod
    def activate_iterface(cls):
        cls.access_point.active(True)
        cls.station.active(True)

