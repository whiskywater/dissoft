import subprocess
import time
import os
import re

def get_interface():
    # Prompt user for the network interface
    interface = input("Enter the network interface (e.g., wlan0, wlo1): ")
    return interface

def scan_wifi(interface):
    # Command to scan wifi networks
    command = ['iwlist', interface, 'scan']
    try:
        # Execute the command
        scan_output = subprocess.check_output(command, universal_newlines=True)
        return scan_output
    except subprocess.CalledProcessError as e:
        print(f"Failed to scan networks: {e}")
        return "FAILED SCAN, IGNORE"

def parse_and_save(scan_data, file):
    if scan_data:
        # Current timestamp
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        network_info = {}
        first_network = True
        seen_networks = set()  # To keep track of networks and avoid duplicates

        for line in scan_data.splitlines():
            if 'Cell' in line:  # New network block starts
                if network_info:  # If there's accumulated network info, write it down
                    essid = network_info.get('ESSID', 'Unknown')
                    if essid != 'Unknown' and essid not in seen_networks:
                        seen_networks.add(essid)
                        if first_network:  # For the first network, add the scan time
                            file.write(f"Scan Time: {current_time}\n")
                            first_network = False
                        file.write(f"ESSID: {essid}\n")
                        file.write(f"Channel: {network_info.get('Channel', 'Unknown')}\n")
                        file.write(f"Signal Strength: {network_info.get('Signal Strength', 'Unknown')}\n")
                        file.write(f"Security: {network_info.get('Security', 'Unknown')}\n")
                    network_info = {}  # Reset for the next network

            if 'ESSID' in line and line.split(':')[1].strip():
                essid = line.split(':')[1].strip().strip('"')
                network_info['ESSID'] = essid
            elif 'Address' in line:
                # Extract MAC address
                network_info['Address'] = line.split(' ')[-1].strip()
            elif 'Frequency' in line:
                # Extracting channel from frequency
                match = re.search(r'(\d+\.\d+) GHz \(Channel (\d+)\)', line)
                if match:
                    network_info['Channel'] = match.group(2)
            elif 'Quality' in line or 'Signal level' in line:
                # Extract signal strength
                signal_strength = line.split('=')[1].split(' ')[0]
                network_info['Signal Strength'] = signal_strength
            elif 'Encryption key' in line:
                # Extract encryption key information
                if 'on' in line:
                    network_info['Security'] = 'Encrypted'
                else:
                    network_info['Security'] = 'Open'
            elif 'IE: IEEE' in line and 'WPA' in line or 'WPA2' in line:
                # Extract detailed security type
                security_type = line.split(':')[1].strip()
                network_info['Security'] = security_type

        # Write the last network entry if it exists and wasn't written yet
        if network_info:
            essid = network_info.get('ESSID', 'Unknown')
            if essid != 'Unknown' and essid not in seen_networks:
                if first_network:
                    file.write(f"Scan Time: {current_time}\n")
                file.write(f"ESSID: {essid}\n")
                file.write(f"Channel: {network_info.get('Channel', 'Unknown')}\n")
                file.write(f"Signal Strength: {network_info.get('Signal Strength', 'Unknown')}\n")
                file.write(f"Security: {network_info.get('Security', 'Unknown')}\n")
                file.write('=' * 32 + '\n')

def main():
    interface = get_interface()
    # Open the output file in append mode
    with open('output.txt', 'a') as file:
        try:
            while True:
                scan_data = scan_wifi(interface)
                if scan_data:  # Ensure data is only written if scan was successful
                    parse_and_save(scan_data, file)
                time.sleep(60)  # Adjust scan interval to a reasonable duration
        except KeyboardInterrupt:
            print("Stopped by user.")

if __name__ == "__main__":
    main()
