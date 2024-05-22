import subprocess
import re

def scan_wifi():
    # Command to scan Wi-Fi; 'wlan0' is a common interface name for Wi-Fi devices
    command = ["sudo", "iwlist", "wlan0", "scan"]
    
    # Running the command
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        networks = []
        
        # Regular expression to find SSIDs
        ssid_pattern = re.compile(r'ESSID:"(.*?)"')
        strength_pattern = re.compile(r'Signal level=(\d+)')

        for line in result.stdout.split('\n'):
            ssid_search = ssid_pattern.search(line)
            strength_search = strength_pattern.search(line)
            if ssid_search and strength_search:
                networks.append((ssid_search.group(1), strength_search.group(1)))
        
        return networks
    except subprocess.CalledProcessError as e:
        print("Failed to scan networks:", e)
        return []

# Example usage
networks = scan_wifi()
for ssid, strength in networks:
    print(f"SSID: {ssid}, Signal Strength: {strength}")
