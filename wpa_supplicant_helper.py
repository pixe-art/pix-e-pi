import subprocess

def scan_networks():
    scan = subprocess.run(["wpa_cli", "-i", "wlan0", "scan"], capture_output=True, text=True) 
    scan_result = subprocess.run(["wpa_cli", "-i", "wlan0", "scan_result"], capture_output=True, text=True)
    scan_string = scan_result.stdout
    lines = scan_string.split("\n")
    networks = []

    print(scan_string)

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
    
    return deduped_networks
