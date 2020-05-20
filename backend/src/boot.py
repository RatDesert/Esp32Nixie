from wifi import Wifi
import ulogging as logging
from server import app
from utils import DB
from hardware import Led
import json

#set MCU as access point
Wifi.activate_iterface()
Wifi.set_ap_conf(essid='test', password='test1234')

#set led color
color = json.loads(DB.fetch(b"led").decode())
r, g, b = color['r'], color['g'], color['b']
Led.change_color({x: (r, g, b) for x in range(6)})
#must set time via internet if connected and auto-time is true

#close db
logging.basicConfig(level=logging.INFO)

#logging.basicConfig(level=logging.DEBUG)


# debug values:
# -1 disable all logging
# 0 (False) normal logging: requests and errors
# 1 (True) debug logging
# 2 extra debug logging
app.run(debug=1, host="0.0.0.0", port=80)