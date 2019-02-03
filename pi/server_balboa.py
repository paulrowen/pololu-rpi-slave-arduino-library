#!/usr/bin/env python3

# Copyright Pololu Corporation.  For more information, see https://www.pololu.com/
from flask import Flask
from flask import render_template
from flask import redirect
from subprocess import call
app = Flask(__name__, static_folder='server_balboa_resources/static', template_folder='server_balboa_resources/templates')
app.debug = True

import sys

from a_star import AStar
a_star = AStar()

from ST_VL6180X import VL6180X

debug = False

tof_address = 0x29
tof_sensor = VL6180X(address=tof_address, debug=debug)
# apply pre calibrated offset
tof_sensor.set_range_offset(23)
tof_sensor.default_settings()

from balance import Balancer
balancer = Balancer()

tof_distance = 255

import json

led0_state = False
led1_state = False
led2_state = False

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/status.json")
def status():
    buttons = a_star.read_buttons()
    analog = a_star.read_analog()
    battery_millivolts = a_star.read_battery_millivolts()
    encoders = a_star.read_encoders()
    calibrated = balancer.calibrated
    tof_distance = tof_sensor.get_distance()
    tof_lux = round(tof_sensor.get_ambient_light(20), 2)
    data = {
        "buttons": buttons,
        "battery_millivolts": battery_millivolts,
        "analog": analog,
        "encoders": encoders,
        "calibrated": calibrated,
        "tof_distance": tof_distance,
        "tof_lux": tof_lux
    }
    return json.dumps(data)

@app.route("/calibrate")
def calibrate():
    balancer.setup()
    balancer.start()
    return ""

@app.route("/stand_up")
def stand_up():
    balancer.stand_up()
    return ""

@app.route("/drive_test")
def drive_test():
    tof_distance = tof_sensor.get_distance()
    if (tof_distance > 254):
        # move forwards until an object appears
        drive(-10,-10)
        tof_distance = tof_sensor.get_distance()      
    elif (tof_distance < 255):
        play_notes("l16def>d")
        # then turn
        drive(-10,10)
        time.sleep(0.2)
        #then drive forwards
        drive(-10,-10)
        tof_distance = tof_sensor.get_distance()

@app.route("/drive/<left>,<right>")
def drive(left, right):
    balancer.drive(int(left), int(right))
    return ""

@app.route("/leds/<int:led0>,<int:led1>,<int:led2>")
def leds(led0, led1, led2):
    a_star.leds(led0, led1, led2)
    global led0_state
    global led1_state
    global led2_state
    led0_state = led0
    led1_state = led1
    led2_state = led2
    return ""

@app.route("/heartbeat/<int:state>")
def hearbeat(state):
    if state == 0:
      a_star.leds(led0_state, led1_state, led2_state)
    else:
        a_star.leds(not led0_state, not led1_state, not led2_state)
    return ""

@app.route("/play_notes/<notes>")
def play_notes(notes):
    a_star.play_notes(notes)
    return ""

@app.route("/halt")
def halt():
    call(["bash", "-c", "(sleep 2; sudo halt)&"])
    return redirect("/shutting-down")

@app.route("/shutting-down")
def shutting_down():
    return "Shutting down in 2 seconds! You can remove power when the green LED stops flashing."

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
