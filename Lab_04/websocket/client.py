import tornado.ioloop
import tornado.websocket

class WebSocketClient:
    # Lớp WebSocket client để kết nối với WebSocket server
    def __init__(self, io_loop):
        self.connection = None  # Biến lưu trữ kết nối WebSocket
        self.io_loop = io_loop  # Vòng lặp sự kiện IOLoop

    def start(self):
        # Bắt đầu kết nối với server
        self.connect_and_read()

    def stop(self):
        # Dừng vòng lặp sự kiện
        self.io_loop.stop()

    def connect_and_read(self):
        # Thực hiện kết nối tới WebSocket server
        print("Connecting...")
        tornado.websocket.websocket_connect(
            url="ws://localhost:8888/websocket/",  # Địa chỉ WebSocket server
            callback=self.maybe_retry_connection,  # Callback xử lý khi kết nối
            on_message_callback=self.on_message,  # Callback nhận tin nhắn
            ping_interval=10,  # Khoảng thời gian gửi ping
            ping_timeout=30,   # Thời gian chờ phản hồi trước khi ngắt kết nối
        )

    def maybe_retry_connection(self, future):
        # Xử lý kết nối, nếu thất bại thì thử lại sau 3 giây
        try:
            self.connection = future.result()  # Nhận kết quả từ Future
            print("Connected to server")
            self.connection.read_message(callback=self.on_message)  # Đọc tin nhắn đầu tiên
        except Exception as e:
            print("Could not connect, retrying in 3 seconds...")
            self.io_loop.call_later(3, self.connect_and_read)  # Thử lại sau 3 giây

    def on_message(self, message):
        # Nhận và xử lý tin nhắn từ server
        if message is None:  # Nếu mất kết nối
            print("Disconnected, reconnecting...")
            self.connect_and_read()  # Thử kết nối lại
            return
        print(f"Received word from server: {message}")  # Hiển thị tin nhắn nhận được
        self.connection.read_message(callback=self.on_message)  # Đọc tin nhắn tiếp theo

def main():
    # Khởi động WebSocket client
    io_loop = tornado.ioloop.IOLoop.current()  # Lấy vòng lặp sự kiện hiện tại
    client = WebSocketClient(io_loop)  # Khởi tạo client
    io_loop.add_callback(client.start)  # Thêm client vào vòng lặp
    io_loop.start()  # Bắt đầu vòng lặp

if __name__ == "__main__":
    main()
