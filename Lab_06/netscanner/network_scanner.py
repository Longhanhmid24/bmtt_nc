import requests
from scapy.all import ARP, Ether, srp

def local_network_scan(ip_range):
   
    # Create an ARP request packet
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

def get_vendor_mac(mac):
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}")
        if response.status_code == 200:
            return response.text
        else:
            return "Unknown"
    except Exception as e:
        print("Error fetching vendor info: ", e)
        return "Unknown"

def main():
    ip_range = "192.168.26.69/24"
    devices = local_network_scan(ip_range)

    print("Devices found in the network:")
    for device in devices:
        mac = device['mac']
        vendor = get_vendor_mac(mac)
        print(f"IP: {device['ip']}, MAC: {mac}, Vendor: {vendor}")

if __name__ == "__main__":
    main()
    

