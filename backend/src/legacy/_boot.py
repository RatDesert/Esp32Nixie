from hardware import Led, set_rtc_date
import network
import time
import gc

class Wifi:
    station = network.WLAN(network.STA_IF)
    access_point = network.WLAN(network.AP_IF)
    station.active(True)
    access_point.active(True)

    def set_ap_conf(self ,essid, password):
        self.access_point.config(essid=essid, password=password, authmode=3)

    def scann(self):
        return tuple((item[0], item[3]) for item in self.station.scan())

    def connect(self, login, password):
        self.station.connect(login, password)

        time_start = time.time()

        while time.time() - time_start < 10:
            if self.station.isconnected():
                print('connected || ', self.station.ifconfig())
                break
        else:
            print('WifiNotAuth')
            raise Exception




if __name__ == '__main__':
    USER_WIFI_ESSID = 'RatDesert'
    USER_WIFI_PASSWORD = '32fdsDSFds14DAs'

    AP_ESSID = 'test'
    AP_PASSWORD = 'test1234'

    
    wifi = Wifi()
    
    wifi.set_ap_conf(essid=AP_ESSID, password=AP_PASSWORD)
    # result = wifi.scann()

    # print(result)

    # wifi.connect(USER_WIFI_ESSID, USER_WIFI_PASSWORD)


    colors = {x: (25, 0, 15) for x in range(6)}
    Led.change_color(colors)
    set_rtc_date()

    # from microhttp import WebApp, Response, status

    # def index(request):
    #     yield from Response(status=status.OK_200 ,content_type='/static/index.html', file_path='/static/index.html')


    # def lamps(request):
    #     yield from Response(status=status.OK_200 ,content_type='text/html', file_path='/static/lamps.html')

    # def login(request):
    #     print(request.data)
    #     yield from Response(status=status.CREATED_201 ,content_type='text/html', file_path='/static/index.html')

    # def led(request):
    #     print(request.data)
    #     color = request.data
    #     color = color.split('&')
    #     color = tuple(int(x.split('=')[1]) for x in color)
    #     Led.change_color({x: color for x in range(6)})

    #     yield from Response(status=status.CREATED_201 ,content_type='text/html', file_path='/static/lamps.html')

    # def off(request):
    #     import sys
    #     gc.collect()
    #     yield from Response(status=status.ACCEPTED_202)
    #     yield sys.exit()

    # web_app = WebApp()
    # web_app.handlers = {'/': ['GET' ,index], '/lamps': ['GET', lamps], '/login':['POST', login], '/led':['POST', led], '/off':['GET', off]}

    # web_app.run()