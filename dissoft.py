import subprocess
import re

def get_wireless_interface():
    # Command to list network interfaces
    try:
        result = subprocess.run(["ip", "link"], capture_output=True, text=True, check=True)
        # Regular expression to find wireless network interfaces, commonly start with 'wl'
        interface_pattern = re.compile(r'\d+: (wl\w+):')

        # Searching for wireless interface names
        interfaces = interface_pattern.findall(result.stdout)
        if interfaces:
            return interfaces[0]  # Return the first wireless interface found
        else:
            print("No wireless interface found.")
            return None
    except subprocess.CalledProcessError as e:
        print("Failed to list network interfaces:", e)
        return None

def scan_wifi(interface):
    if interface is None:
        return []
    # Command to scan Wi-Fi
    command = ["sudo", "iwlist", interface, "scan"]

    # Running the command
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        networks = []

        # Regular expressions to find SSIDs and signal strength
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

# Finding the wireless interface
wireless_interface = get_wireless_interface()

# Scanning Wi-Fi networks
networks = scan_wifi(wireless_interface)
for ssid, strength in networks:
    print(f"SSID: {ssid}, Signal Strength: {strength}")
