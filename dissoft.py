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
        # Instead of returning None, return an empty string to avoid affecting the output file
        return "FAILED SCAN, IGNORE"

def parse_and_save(scan_data, file):
    if scan_data:
        # Write current timestamp
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file.write(f"Scan Time: {current_time}\n")
        
        network_info = {}
        for line in scan_data.splitlines():
            if 'Cell' in line:  # New network block starts
                if network_info:  # Save previous block if it exists
                    file.write(f"ESSID: {network_info.get('ESSID', 'Unknown')}\n")
                    file.write(f"MAC Address: {network_info.get('Address', 'Unknown')}\n")
                    file.write(f"Channel: {network_info.get('Channel', 'Unknown')}\n")
                    file.write('=' * 32 + '\n')
                    network_info = {}  # Reset for next network block

            if 'ESSID' in line:
                essid = line.split(':')[1].strip().strip('"')
                network_info['ESSID'] = essid
            elif 'Address' in line:
                address = line.split(' ')[-1].strip()
                network_info['Address'] = address
            elif 'Frequency' in line:
                # Extracting channel from frequency
                match = re.search(r'(\d+\.\d+) GHz \(Channel (\d+)\)', line)
                if match:
                    network_info['Channel'] = match.group(2)

        # Write the last network entry if exists
        if network_info:
            file.write(f"ESSID: {network_info.get('ESSID', 'Unknown')}\n")
            file.write(f"MAC Address: {network_info.get('Address', 'Unknown')}\n")
            file.write(f"Channel: {network_info.get('Channel', 'Unknown')}\n")
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
                time.sleep(0)  # Pause for 0 second before next scan (troll face moment)
        except KeyboardInterrupt:
            print("Stopped by user.")

if __name__ == "__main__":
    main()
