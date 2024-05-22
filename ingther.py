def read_network_data(file_path):
    network_dict = {}
    current_network = {}
    essid_key = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if 'ESSID:' in line:
                # Save the last network if there is one and it's not a duplicate
                if current_network and essid_key and essid_key not in network_dict:
                    network_dict[essid_key] = current_network

                # Extract ESSID safely
                essid_parts = line.split('ESSID: ')
                if len(essid_parts) > 1:
                    essid_key = essid_parts[1].strip().strip('"')
                    current_network = {}
                else:
                    essid_key = None  # Invalid line format, ignore this network

            elif 'MAC Address:' in line and essid_key:
                mac_parts = line.split('MAC Address: ')
                if len(mac_parts) > 1:
                    current_network['MAC Address'] = mac_parts[1].strip()

            elif 'Channel:' in line and essid_key:
                channel_parts = line.split('Channel: ')
                if len(channel_parts) > 1:
                    current_network['Channel'] = channel_parts[1].strip()

            elif 'Security:' in line and essid_key:
                security_parts = line.split('Security: ')
                if len(security_parts) > 1:
                    current_network['Security'] = security_parts[1].strip()

        # Save the last network entry if valid
        if essid_key and essid_key not in network_dict and current_network:
            network_dict[essid_key] = current_network

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
