import psutil
import time
import platform
import socket
import logging

# Cấu hình logging
logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Hàm ghi log
def log_info(category, message):
    logger.info(f"{category}: {message}")
    print(f"{category}: {message}")

# Hàm giám sát CPU và bộ nhớ
def monitor_cpu_memory():
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()

    log_info("CPU", f"Usage: {cpu_percent}%")
    log_info("Memory", f"Usage: {memory.percent}%")  # Sửa lỗi `memory_info.percent`

# Hàm giám sát thông tin hệ thống
def monitor_system_info():
    os_info = platform.uname()
    hostname = socket.gethostname()

    log_info("System Info", f"Hostname: {hostname}")
    log_info("System Info", f"Operating System: {os_info.system} {os_info.release}")
    log_info("System Info", f"Python Version: {platform.python_version()}")

# Hàm giám sát tình trạng mạng
def monitor_network():
    net_stats = psutil.net_io_counters()
    log_info("Network", f"Bytes Sent: {net_stats.bytes_sent} , Bytes Received: {net_stats.bytes_recv}")

# Hàm giám sát danh sách phần mềm đang chạy
def monitor_processes():
    software_list = psutil.process_iter(attrs=['pid', 'name', 'username'])

    log_info("Software", "Running Software:")
    for process in software_list:
        software_name = process.info['name']
        software_pid = process.info['pid']
        software_username = process.info['username']
        log_info("Software", f"PID: {software_pid}, Name: {software_name}, User: {software_username}")

# Hàm thực hiện giám sát toàn bộ hệ thống
def monitor_system():
    log_info("System Monitor", "Starting system monitoring...")

    while True:
        monitor_system_info()  # Sửa lỗi dòng 51
        monitor_network()
        monitor_cpu_memory()
        monitor_processes()  # Sửa lỗi dòng 62
        log_info("System Monitor", "-------------------------------------------------")
        time.sleep(60)

if __name__ == "__main__":
    monitor_system()
