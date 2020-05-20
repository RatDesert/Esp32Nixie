from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from fastapi.responses import JSONResponse
import time
import uvicorn
from fastapi.encoders import jsonable_encoder
import os

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
    'http://192.168.1.104:8000',
    '*'
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#LED
LED_COLOR = {'r':0, 'g':0, 'b':0}

class LedColor(BaseModel):
    r: int
    g: int
    b: int

@app.get('/led/')
async def get_led_color():
    return JSONResponse(status_code=status.HTTP_200_OK, content=LED_COLOR)

@app.post('/led/')
async def change_led_color(color: LedColor):
    
    LED_COLOR['r'], LED_COLOR['g'], LED_COLOR['b'] = color.r, color.g, color.b
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=LED_COLOR)

#WIFI
ACTIVE_WIFI = {'essid': None}


class WifiAuth(BaseModel):
    essid: str
    password: str = None


@app.post('/wifi/', status_code=201)
async def connect_to_wifi(wifi: WifiAuth):
    if wifi.password == 'lol123':
        ACTIVE_WIFI['essid'] = wifi.essid
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={'essid':wifi.essid})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)

@app.get('/wifi/')
async def get_wifi_list():
    time.sleep(2)
    ap_list = [{ 'essid': "KiberSportArena", 'rssi': -49, 'security': 1 },
            { 'essid': "TP_LINK_6a42", 'rssi': -50, 'security': 4 },
            { 'essid': "TP_link_ewercz", 'rssi': -59, 'security': 4 },
            { 'essid': "TP_link_ef45vz", 'rssi': -60, 'security': 4 },
            { 'essid': "TP_link_7nxza", 'rssi': -71, 'security': 4 },
            { 'essid': "TP_link_45gx", 'rssi': -49, 'security': 4 },
            { 'essid': "TP_link_5unx", 'rssi': -49, 'security': 4 },
            { 'essid': "TP_link_m5c", 'rssi': -49, 'security': 4 },
            { 'essid': "TP_link_sdf3", 'rssi': -49, 'security': 4 },
            { 'essid': "TP_link_4fgd", 'rssi': -49, 'security': 4 },
            { 'essid': "TP_link_dfg4", 'rssi': -49, 'security': 4 },
            { 'essid': "TP_link_34sd1", 'rssi': -49, 'security': 4 },
            { 'essid': "TP_link_231", 'rssi': -49, 'security': 4 },
            { 'essid': "TP_link_2d1", 'rssi': -49, 'security': 4 },
            { 'essid': "TP_link_2j1", 'rssi': -49, 'security': 4 }
    ]
    random.shuffle(ap_list)
    return ap_list

@app.get('/wifi/active/')
async def active_ap():
    return JSONResponse(status_code=status.HTTP_200_OK, content=ACTIVE_WIFI)

#STATE
CLOCK_STATE = {'first_setup': True, 'auto_time': False}


class AutoTime(BaseModel):
    auto_time: bool

class FirstSetup(BaseModel):
    first_setup: bool

@app.get('/settings/firstsetup/')
async def get_setup_state():
    return JSONResponse(status_code=status.HTTP_200_OK, content={'first_setup':CLOCK_STATE['first_setup']})

@app.get('/settings/autotime/')
async def get_setup_state():
    return JSONResponse(status_code=status.HTTP_200_OK, content={'auto_time':CLOCK_STATE['auto_time']})

@app.post('/settings/firstsetup/')
async def post_setup_state(state:FirstSetup):

    CLOCK_STATE['first_setup'] = state.first_setup
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'first_setup':CLOCK_STATE['first_setup']})

@app.post('/settings/autotime/')
async def post_setup_state(state:AutoTime):

    CLOCK_STATE['auto_time'] = state.auto_time
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'auto_time':CLOCK_STATE['auto_time']})

@app.get("/server/off/")
async def turn_off_server():
    print("kek")
    os._exit(0)



#DATE
CLOCK_DATE = {}


class ClockDate(BaseModel):
    year:int
    month: int
    day: int
    weekday: int
    hour: int
    minute: int
    second: int
    milliseconds: int = None

class ClockTime(BaseModel):
    hour: int
    minute: int
    second: int


@app.post('/date/')
async def set_clock_date(date: ClockDate):
    date = jsonable_encoder(date)
    global CLOCK_DATE
    CLOCK_DATE.update(date)
    print(CLOCK_DATE)
    return JSONResponse(status_code=status.HTTP_201_CREATED)

@app.get('/date/')
async def get_clock_date():
    print(CLOCK_DATE)
    return JSONResponse(status_code=status.HTTP_200_OK, content=CLOCK_DATE)

@app.post('/date/time/')
async def set_clock_time(time:ClockTime):
    print(time)
    CLOCK_DATE.update(time)
    return JSONResponse(status_code=status.HTTP_201_CREATED)



if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='debug')