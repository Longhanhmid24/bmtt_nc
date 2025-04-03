import psutil
import time
import logging
import asyncio
from telegram import Bot

#Thay thep token cua ban vao day
BOT_TOKEN= '7928283698:AAHDeuExNWQLe5ZKCHo-2Rv_k32BeZ_xiHc' #<======== TOKEN MỖI NGƯỜI KHÁC NHAU TỰ THAY ĐỔI#
#Thay thep id cua ban vao day
CHAT_ID= '-4799887070' #<======== ID MỖI NGƯỜI KHÁC NHAU TỰ THAY ĐỔI#

# Cấu hình logging
logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Hàm ghi log
def log_info(category, message):
    logger.info(f"{category}: {message}")
    print(f"{category}: {message}")

# Hàm gửi tin nhắn đến Telegram
async def send_telegram_message(message):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

# Hàm giám sát CPU và bộ nhớ
def monitor_cpu_memory():
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()

    log_info("CPU", f"Usage: {cpu_percent}%")
    log_info("Memory", f"Usage: {memory_info.percent}%")

    # Gửi thông báo đến Telegram
    message = f"CPU Usage: {cpu_percent}%, Memory Usage: {memory_info.percent}%"
    asyncio.run(send_telegram_message(message))

# Hàm giám sát thông tin hệ thống
def monitor_system_info():
    log_info("System Monitor", "Starting system monitoring...")

    while True:
        monitor_cpu_memory()
        log_info("System Monitor", "-------------------------------------------------")
        time.sleep(60)

if __name__ == "__main__":
    monitor_system_info()