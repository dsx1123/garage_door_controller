#!/usr/bin/env python

__author__= "Shangxin Du"
__email__="shangxindu@gmail.com"

import logging
import time
from datetime import datetime
import json
from logging.handlers import RotatingFileHandler
from threading import Timer

from gpiozero import Button,OutputDevice
from flask import Flask, current_app

app=Flask(__name__)

class Door():
    last_action = None 

    def __init__(self,  config):
            self.name = config['door']['name']
            self.pin_relay = config['door']['pin_relay']
            self.pin_state = config['door']['pin_state']
            self.time_to_open = config['door']['time_to_open']
            self.time_to_close = config['door']['time_to_close']
            self.switch = Button(self.pin_state)
            self.opener = OutputDevice(self.pin_relay,False,False)
            self.switch_thread =None
            self.last_trigger_time = datetime.today()
            self.state = "close"

    def get_state(self):
        if self.switch.is_pressed == 0 :
            self.state = "close"
        return self.state

    def set_state(self,state):
        print("set state to: {}".format(state))
        self.state = state

    def trigger_switch(self):
        print(self.opener.value)
        self.opener.on()
        time.sleep(3)
        self.opener.off()
        self.last_trigger_time = datetime.today()
        state = self.get_state()

        if self.state == "close":
            self.switch_thread= Timer(self.time_to_open, self.set_state, [ "open",])
            self.switch_thread.start()
            self.state = "openning"
        elif self.state == "openning":
            self.switch_thread.cancel()
            self.state = "open" 
        elif self.state == "open": 
            self.switch_thread= Timer(self.time_to_close, self.set_state, ["close",])
            self.switch_thread.start() 
            self.state = "closing" 
        elif self.state == "closing":
            self.switch_thread.cancel()
            self.state = "open"
        return self.state

    def get_trigger_time(self):
        time_format = "%Y-%m-%dT%H:%M:%S"
        return str(self.last_trigger_time.strftime(time_format))

def init_app(app):
    app.debug = True
    config = None
    with open('config.json','r') as f:
        try:
            config = json.load(f)
        except ValueError as e:
            app.logger.error(e)
    with app.app_context():
        current_app.config["door"]= Door(config)

init_app(app)

@app.route("/app/state")
def get_state():
    with app.app_context():
        door= current_app.config["door"]
        return door.get_state()
        

@app.route("/app/trigger")
def trigger():
    with app.app_context():
        state = current_app.config["door"].trigger_switch()
        print(state)
        return state

@app.route("/app/trigger_time")
def trigger_time():
    with app.app_context():
        door= current_app.config["door"]
        return door.get_trigger_time()


