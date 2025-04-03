from scapy.all import IP, TCP, sr, sr1
import socket


COMMON_PORTS = [ 21, 22, 23, 25, 53, 80, 110, 143, 443, 8080 ]

def scan_common_ports(target_domain, timeout=2):
    open_ports = []
    target_ip = socket.gethostbyname(target_domain)

    for port in COMMON_PORTS:
        response = sr1(IP(dst=target_ip)/TCP(dport=port, flags="S"), timeout=timeout, verbose=0)

        if response and response.haslayer(TCP) and response[TCP].flags == 0x12:
            open_ports.append(port)
            sr(IP(dst=target_ip)/TCP(dport=port, flags="R"), timeout=timeout, verbose=0)

    return open_ports

def main():
    target_domain = input("Nhập tên miền hoặc địa chỉ IP: ")
    
    open_ports = scan_common_ports(target_domain)

    if open_ports:
        print(f"Các cổng mở trên :")
        print(open_ports)
    else:
        print("Không có cổng nào mở.")

if __name__ == "__main__":
    main()