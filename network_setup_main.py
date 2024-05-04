import connectivity_check
import hostapd_helper
import time
import subprocess
import requests
import atexit

flask_running = False
global flask_process
hostapd_running = False
dnsmasq_running = False

while True:
    print("loop")
    stat = subprocess.call(["systemctl", "is-active", "--quiet", "hostapd"])
    if(stat == 0):  # if 0 (active), print "Active"
        hostapd_running = True
        print("hostapd running")
    else:
        hostapd_running = False
        print("hostapd not running")
    
    stat = subprocess.call(["systemctl", "is-active", "--quiet", "dnsmasq"])
    if(stat == 0):  # if 0 (active), print "Active"
        dnsmasq_running = True
        print("dnsmasq running")
    else:
        dnsmasq_running = False
        print("dnsmasq not running")

    try:
        print("requesting")
        r = requests.get("http://127.0.0.1/api/ping", timeout=10)
        print("requested")
        if r.status_code == 200:
            flask_running = True
            print("flask running")
        else:
            flask_running = False
            print("flask not running")
    except Exception as e:
        flask_running = False
        print("flask not running")

    if connectivity_check.is_connected():
        print("connected")
        if flask_running:
            print("flask running, terminating")
            flask_process.terminate()

        if hostapd_running or dnsmasq_running:
            print("ap running, terminating")
            hostapd_helper.disable_ap()
    else:
        print("not connected")
        if not (hostapd_running and dnsmasq_running):
            print("ap not running, starting")
            hostapd_helper.enable_ap()

        if not flask_running:
            print("flask not running, starting")
            flask_process = subprocess.Popen(['/home/pi/.local/share/virtualenvs/pix-e-HnRFVe-M/bin/python', 'network_setup_web.py'], shell=True)
    print("network setup sleeping 30 seconds")
    time.sleep(30)
    # for i in range(30):
    #     print(i)
    #     time.sleep(1)


def cleanup():
    flask_process.terminate()

atexit.register(cleanup)