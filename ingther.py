def read_network_data(file_path):
    network_dict = {}
    with open(file_path, 'r') as file:
        data = file.read().split('Scan Time: ')[1:]  # Split into blocks starting from second block to skip header
        for block in data:
            lines = block.split('\n')
            essid = ''
            for line in lines:
                if 'ESSID: ' in line:
                    essid = line.split('ESSID: ')[1].strip()
                elif 'MAC Address: ' in line and essid:
                    mac_address = line.split('MAC Address: ')[1].strip()
                elif 'Channel: ' in line and essid:
                    channel = line.split('Channel: ')[1].strip()
                elif 'Security: ' in line and essid:
                    security = line.split('Security: ')[1].strip()
            if essid and essid not in network_dict:  # Avoid duplicates
                network_dict[essid] = {
                    'MAC Address': mac_address,
                    'Channel': channel,
                    'Security': security
                }
    return network_dict

def get_network_info(ssid, network_dict):
    info = network_dict.get(ssid)
    if info:
        print(f"Details for SSID '{ssid}':")
        print(f"MAC Address: {info['MAC Address']}")
        print(f"Channel: {info['Channel']}")
        print(f"Security: {info['Security']}")
    else:
        print(f"No information found for SSID '{ssid}'.")

def main():
    ssid_input = input("Enter the SSID you want to look up: ")
    network_dict = read_network_data('output.txt')
    get_network_info(ssid_input, network_dict)

if __name__ == "__main__":
    main()
