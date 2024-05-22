import subprocess

def scan_wifi():
    # Command to scan wifi networks; 'wlan0' is the common name of the wireless interface on Linux
    command = ['iwlist', 'wlan0', 'scan']
    try:
        # Execute the command
        scan_output = subprocess.check_output(command, universal_newlines=True)
        return scan_output
    except subprocess.CalledProcessError as e:
        print(f"Failed to scan networks: {e}")
        return None

def parse_and_save(scan_data):
    if scan_data:
        # Open the output file
        with open('output.txt', 'w') as file:
            for line in scan_data.splitlines():
                # Look for lines containing 'ESSID' which is the name of the WiFi network
                if 'ESSID' in line:
                    file.write(line.strip() + '\n')

def main():
    scan_data = scan_wifi()
    if scan_data:
        parse_and_save(scan_data)
    else:
        print("No scan data available.")

if __name__ == "__main__":
    main()
