import subprocess
import time
import os

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
        return ""

def parse_and_save(scan_data, file):
    if scan_data:
        # Write current timestamp
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file.write(f"Scan Time: {current_time}\n")
        
        # Write each network's ESSID
        for line in scan_data.splitlines():
            if 'ESSID' in line:
                file.write(line.strip() + '\n')
        
        # Separator for clusters of entries
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
                time.sleep(1)  # Pause for 1 second before next scan
        except KeyboardInterrupt:
            print("Stopped by user.")

if __name__ == "__main__":
    main()
