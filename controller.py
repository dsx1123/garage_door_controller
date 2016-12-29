#!/usr/bin/env python

__author__= "Shangxin Du"
__email__="shangxindu@gmail.com"

import logging
import time
import json
from logging.handlers import RotatingFileHandler
from threading import Timer

from gpiozero import Button,OutputDevice
from flask import Flask, g

class Door():
    last_action = None
    last_trigger_time = None

    def __init__(self,  config):
            self.name = config['door']['name']
            self.pin_relay = config['door']['pin_relay']
            self.pin_state = config['door']['pin_state']
            self.time_to_open = config['door']['time_to_open']
            self.time_to_close = config['door']['time_to_close']
            self.switch = Button(self.pin_state)
            self.state = "close"

    def get_state(self):
        if self.switch.is_pressed == 0 :
            self.state = "close"
        return self.state

    def set_state(self,state):
        print("set state to: {}".format(state))
        self.state = state

    def trigger_switch(self):
        switch = OutputDevice(self.pin_relay)
        time.sleep(0.5)
        switch.on()

        state = self.get_state()
        global switch_thread
        if self.state == "close":
            switch_thread= Timer(self.time_to_open, self.set_state, [ "open",])
            switch_thread.start()
            self.state = "openning"
        elif self.state == "openning":
            switch_thread.cancel()
            self.state = "open" 
        elif self.state == "open": 
            switch_thread= Timer(self.time_to_close, self.set_state, ["close",])
            switch_thread.start() 
            self.state = "closing" 
        elif self.state == "closing":
            switch_thread.cancel()
            self.state = "open"
        return self.state

def init_app():
    app = Flask(__name__)
    config = None
    print("Initializing...")
    with open('config.json','r') as f:
        try:
            config = json.load(f)
        except ValueError as e:
            app.logger.error(e)
    with app.app_context():
        g.garage_door = Door(config)
    handler = RotatingFileHandler('/var/log/garage_door.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    print("Initialzed...")
    return app

app = Flask(__name__)
#app = init_app()




@app.route("/app/state")
def get_state():
    with app.app_context():
        return g.garage_door.get_state()
        

@app.route("/app/trigger")
def trigger():
    with app.app_context():
        state = g.garage_door.trigger_switch()
        print(state)
        return state

if __name__ == "__main__":
    app.run()
