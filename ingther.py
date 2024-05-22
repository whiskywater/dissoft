def read_network_data(file_path):
    network_dict = {}
    current_network = {}
    essid_key = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if 'ESSID:' in line:
                if current_network:  # Save the last network if there is one
                    if essid_key and essid_key not in network_dict:  # Avoid duplicates
                        network_dict[essid_key] = current_network
                # Reset for new network
                essid_key = line.split('ESSID: ')[1].strip().strip('"')
                current_network = {}
            elif 'MAC Address:' in line and essid_key:
                current_network['MAC Address'] = line.split('MAC Address: ')[1].strip()
            elif 'Channel:' in line and essid_key:
                current_network['Channel'] = line.split('Channel: ')[1].strip()
            elif 'Security:' in line and essid_key:
                current_network['Security'] = line.split('Security: ')[1].strip()

        # Make sure to save the last network entry
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
