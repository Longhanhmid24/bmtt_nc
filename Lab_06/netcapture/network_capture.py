import subprocess
from scapy.all import *

def get_interfaces():
    result = subprocess.run(["netsh", "interface", "show", "interface"], capture_output=True, text=True)
    output_lines = result.stdout.splitlines()[3:]
    interfaces = [line.split()[3] for line in output_lines if len(line.split()) >=4]
    return interfaces

def packet_callback(packet):
    if packet.haslayer(Raw):
        print("Captured packet:")
        print(str(packet))

interfaces = get_interfaces()

print("Available network interfaces:")
for i, interface in enumerate(interfaces, start=1):
    print(f"{i}: {interface}")

choice = int(input("Chon mot so giao dien: "))
selected_interface = interfaces[choice - 1]

sniff(iface=selected_interface, prn=packet_callback, filter="tcp")
