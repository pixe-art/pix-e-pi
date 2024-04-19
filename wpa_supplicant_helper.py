import subprocess

WIFI_INTERFACE = "wlan0"

def scan_networks():
    scan = subprocess.run(["wpa_cli", "-i", WIFI_INTERFACE, "scan"], capture_output=True, text=True) 
    scan_result = subprocess.run(["wpa_cli", "-i", WIFI_INTERFACE, "scan_result"], capture_output=True, text=True)
    scan_string = scan_result.stdout
    lines = scan_string.split("\n")
    networks = []

    for i in range(len(lines)-1):
        n = lines[i+1].split("\t")
        if len(n) < 5:
            continue
        if n[4] == '':
            continue
        networks.append((n[4], n[2]))
    return networks

def filter_networks(networks):
    deduped_networks = []
    networks_dict = {}
    for network in networks:
        if network[0] in networks_dict:
            
            if int(network[1]) <= networks_dict[network[0]]:
                continue

        networks_dict[network[0]] = int(network[1])
    
    for ssid, signal in networks_dict.items():
        deduped_networks.append((ssid, signal))

    deduped_networks.sort(key=lambda x: x[1], reverse=True)
    
    return deduped_networks

def generate_network_config(ssid, password=None):
    config_string = f'network={{\n\tssid="{ssid}"\n\t'
    if password == None:
        config_string += "key_mgmt=NONE"
    else:
        config_string += f'psk="{password}"'
    config_string += "\n}\n"
    return config_string

def write_config(config, config_path="/etc/wpa_supplicant/wpa_supplicant.conf"):
    config_header = "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\ncountry=SE\n"
    with open(config_path, "w+") as f:
        f.write(config_header)
        f.write(config)
    
def reload_wpa_supplicant():
    subprocess.run(["ip", "addr", "flush", WIFI_INTERFACE], capture_output=True, text=True)
    subprocess.run(["wpa_cli", "-i", WIFI_INTERFACE, "reconfigure"], capture_output=True, text=True)

print(scan_networks())