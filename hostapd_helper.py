import subprocess

WIFI_INTERFACE = "wlan0"

def enable_ap():
    subprocess.run(["ip", "addr", "flush", WIFI_INTERFACE], capture_output=True, text=True)
    subprocess.run(["systemctl", "start", "dnsmasq"], capture_output=True, text=True)
    subprocess.run(["systemctl", "start", "hostapd"], capture_output=True, text=True)

def disable_ap():
    subprocess.run(["ip", "addr", "flush", WIFI_INTERFACE], capture_output=True, text=True)
    subprocess.run(["systemctl", "stop", "dnsmasq"], capture_output=True, text=True)
    subprocess.run(["systemctl", "stop", "hostapd"], capture_output=True, text=True)