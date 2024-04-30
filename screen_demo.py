from flask import Flask, request, jsonify, redirect
import subprocess
import screen_helper
import hostapd_helper

#hostapd_helper.enable_ap()

app = Flask(__name__)

screen_process = None

def screen(path):
    global screen_process
    if screen_process is not None:
        screen_process.terminate()

    screen_process = screen_helper.display_image(path)

@app.route("/")
def index():
    return app.send_static_file('screen_demo.html')

@app.route("/1", methods=['POST', 'GET'])
def image1():
    screen("/home/pi/img/red.png")
    return "ok"

@app.route("/2", methods=['POST'])
def image2():
    screen("/home/pi/img/green.png")
    return "ok"

@app.route("/3", methods=['POST'])
def image3():
    screen("/home/pi/img/blue.png")
    return "ok"

@app.route("/4", methods=['POST'])
def image4():
    screen("/home/pi/img/rgb.png")
    return "ok"

@app.route("/5", methods=['POST'])
def image5():
    screen("/home/pi/img/test.png")
    return "ok"

app.run(host='0.0.0.0', port=80)
