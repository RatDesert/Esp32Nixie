import json
from hardware import Led, DS1307, set_rtc_date
import sys
import re
import picoweb
from utils import DB
import json
from wifi import Wifi

#files
def index(req, resp):
    yield from app.sendfile(resp, "static/index.html")
    

def styles(req, resp):
    file_path = req.url_match.group(0)
    headers = b"Cache-Control: max-age=86400\r\n"

    if b"gzip" in req.headers.get(b"Accept-Encoding", b""):
        file_path += ".gz"
        headers += b"Content-Encoding: gzip\r\n"

    yield from app.sendfile(resp, "static" + file_path, "text/css", headers)


def scripts(req, resp):
    file_path = req.url_match.group(0)
    headers = b"Cache-Control: max-age=86400\r\n"

    if b"gzip" in req.headers.get(b"Accept-Encoding", b""):
        file_path += ".gz"
        headers += b"Content-Encoding: gzip\r\n"
        
    yield from app.sendfile(resp, "static" + file_path, "text/javascript", headers)

def fonts(req, resp):
    file_path = req.url_match.group(0)
    headers = b"Cache-Control: max-age=86400\r\n"

    yield from app.sendfile(resp, "static" + file_path, "font/woff", headers)

def fonts_2(req, resp):
    file_path = req.url_match.group(0)
    headers = b"Cache-Control: max-age=86400\r\n"

    yield from app.sendfile(resp, "static" + file_path, "font/woff2", headers)
    
#api
#LED
def led(req, resp):
    method = req.method
    if method == "GET":
        print("send_led")
        color = DB.fetch(b"led")
        yield from picoweb.start_response(resp, content_type="application/json", status="200", headers=None)
        yield from resp.awrite(color)

    if method == "POST":
        yield from req.read_body()
        color = json.loads(req.data)
        r, g, b = color['r'], color['g'], color['b']
        Led.change_color({x: (r, g, b) for x in range(6)})
        color = json.dumps({"r":r, "g":g, "b":b}).encode()
        DB.commmit(b"led", color)
        yield from picoweb.start_response(resp, content_type="application/json", status="201", headers=None)
        yield from resp.awrite(req.data)
        
#WIFI
def wifi(req, resp):
    method = req.method
    if method == "GET":
        wifi_ap = json.dumps(Wifi.scann())
        yield from picoweb.start_response(resp, content_type="application/json", status="200", headers=None)
        yield from resp.awrite(wifi_ap)

    if method == "POST":
        
        yield from req.read_body()
        wifi_auth = json.loads(req.data)
        essid = wifi_auth.get("essid")
        password = wifi_auth.get("password")
        result = Wifi.connect(essid, password)
        if result:
            yield from picoweb.start_response(resp, content_type="application/json", status="201", headers=None)
            active_wifi = json.dumps({"essid":Wifi.station.config('essid')})
            yield from resp.awrite(active_wifi)
        else:
            yield from picoweb.start_response(resp, status="400", headers=None)

def active_wifi(req, resp):
    print("send active wifi")
    if  Wifi.station.isconnected():
        active_wifi = json.dumps({"essid":Wifi.station.config('essid')})
    else:
        active_wifi = json.dumps({"essid":""})

    yield from picoweb.start_response(resp, content_type="application/json", status="200", headers=None)
    yield from resp.awrite(active_wifi)
    

#STATE
# def state(req, resp):
#     method = req.method
#     if method == "GET":
#         state = DB.fetch(b"state")
#         yield from picoweb.start_response(resp, content_type="application/json", status="200", headers=None)
#         yield from resp.awrite(state)
#     if method == "POST":
#         yield from req.read_body()
#         user_state = json.loads(req.data)
#         db_state = json.loads(DB.fetch(b"state"))
#         db_state.update(user_state)
#         updated_state = json.dumps(db_state)
#         DB.commmit(b"state", updated_state)
#         yield from picoweb.start_response(resp, content_type="application/json", status="201", headers=None)
#         yield from resp.awrite(updated_state)


def auto_time(req, resp):
    method = req.method
    if method == "GET":
        state = DB.fetch(b"auto_time")
        yield from picoweb.start_response(resp, content_type="application/json", status="200", headers=None)
        yield from resp.awrite(state)
    if method == "POST":
        yield from req.read_body()
        DB.commmit(b"auto_time", req.data)
        yield from picoweb.start_response(resp, content_type="application/json", status="201", headers=None)
        yield from resp.awrite(req.data)

def first_setup(req, resp):
    method = req.method
    if method == "GET":
        state = DB.fetch(b"first_setup")
        yield from picoweb.start_response(resp, content_type="application/json", status="200", headers=None)
        yield from resp.awrite(state)
    if method == "POST":
        yield from req.read_body()
        DB.commmit(b"first_setup", req.data)
        yield from picoweb.start_response(resp, content_type="application/json", status="201", headers=None)
        yield from resp.awrite(req.data)

def _server_off(req, resp):
    sys.exit(0)
    yield from picoweb.start_response(resp, content_type="application/json", status="200", headers=None)
    

def date(req, resp):
    method = req.method
    if method == "GET":
        ds = DS1307()
        date = ds.datetime()
        date = {
                'milliseconds': 0,
                'second': date[6],
                'minute': date[5],
                'hour': date[4],
                'weekday': date[3],
                'day': date[2],
                'month': date[1],
                'year': date[0],
        }

        print('clock__date:', date)
        date = json.dumps(date)
        yield from picoweb.start_response(resp, content_type="application/json", status="200", headers=None)
        yield from resp.awrite(date)

    if method == "POST":
        yield from req.read_body()
        date = json.loads(req.data)
        date = (date['year'], date['month'], date['day'], date['weekday'], date['hour'], date['minute'], date['second'])
        print('formated__date: ', date)
        ds = DS1307()
        ds.datetime(date)
        set_rtc_date()
        yield from picoweb.start_response(resp, status="201", headers=None)

def date_time(req,resp):
    method = req.method
    if method == "POST":
        yield from req.read_body()
        time = json.loads(req.data)
        print('user_time: ', time)
        ds = DS1307()
        date = ds.datetime()
        date = list(date)
        date[4], date[5], date[6] = int(time['hour']), int(time['minute']), int(time['second'])
        print('updated_date: ', date)
        ds.datetime(date)
        set_rtc_date()
        yield from picoweb.start_response(resp, status="201", headers=None)

ROUTES = [
    # You can specify exact URI string matches...
    ("/", index),
    (re.compile('^\/css\/.+.css'), styles),
    (re.compile('^\/js\/.+.js'), scripts),
    (re.compile('^\/fonts\/.+.woff2'), fonts_2),
    (re.compile('^\/fonts\/.+.woff'), fonts),
    ('/wifi/', wifi),
    ('/wifi/active/', active_wifi),
    ('/led/', led),
    ('/settings/autotime/', auto_time),
    ('/settings/firstsetup/', first_setup),
    ('/date/', date),
    ('/date/time/', date_time),
    ('/server/off/', _server_off),


]

app = picoweb.WebApp(__name__, ROUTES)