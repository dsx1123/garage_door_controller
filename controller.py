#!/usr/bin/env python

__author__= "Shangxin Du"
__email__="shangxindu@gmail.com"

import logging
import time
from logging.handlers import RotatingFileHandler
from threading import Thread

from gpiozero import Button,OutputDevice
from flask import Flask

app = Flask(__name__, static_url_path='')

switch_thread = None  


class Door():
    last_action = None
    last_trigger_time = None
def __init__(self,  config):
        self.name = config['name']
        self.pin_relay = config['pin_relay']
        self.pin_state = config['pin_state']
        self.time_to_switch = config['time_to_switch']
        self.switch = Button(self.pin_state)

    def get_state(self):
        """
        Door state:
        close   = 0
        open    = 1
        openning= 2
        closing = 3
        """
        if self.switch.is_pressed == 0 :
            triggered = False
            self.last_action = 0
            return 0
        elif self.last_action == 1 :
            if time.time() - self.last_trigger_time > self.time_to_switch :
                return 1
            else:
                return 2
        elif self.last_action == 0:
            if time.time() - self.last_trigger_time > self.time_to_switch :
                return 1
            else:
                return 3
        else:
            return 1

    def trigger_switch(self):
        switch = OutputDevice(self.pin_relay)
        switch.on()
        time.sleep(0.3)
        switch.off()
        state = self.get_state()
        if  state == 0 :
            self.last_action = 1
            self.last_trigger_time = time.time()
        elif state == 1 :
            self.last_action = 0
            self.last_trigger_time = time.time()
        else:
            self.last_action = None
            self.last_trigger_time = None



@app.route("/door")
def door():
    return '<h1>Hellow There!</h1>'

if __name__ == "__main__":
    garage_door = Door()
    handler = RotatingFileHandler('garage_door.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
