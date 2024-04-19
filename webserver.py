from flask import Flask, request, jsonify, redirect
import json
import wpa_supplicant_helper

app = Flask(__name__)

@app.route("/setup")
def setup():
    return app.send_static_file('index.html')

@app.route("/api/scan")
def web_scan():
    return wpa_supplicant_helper.filter_networks(wpa_supplicant_helper.scan_networks())

@app.route("/api/connect", methods=['POST'])
def web_connect():
    ssid = request.form.get("ssid")
    password = request.form.get("password")
    if password == "":
        password = None
    print(password)
    wpa_supplicant_helper.write_config(wpa_supplicant_helper.generate_network_config(ssid, password))
    wpa_supplicant_helper.reload_wpa_supplicant()
    return "ok"

@app.route("/api/ping")
def ping():
    return "pong", 200

@app.route('/<page>')
def catch_all(page):
    return redirect("/setup", code=302)


app.run(host='0.0.0.0', port=80)