import random
import tornado.ioloop
import tornado.web
import tornado.websocket

# Lớp xử lý kết nối WebSocket
class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()  # Lưu trữ danh sách client đang kết nối

    def open(self):
        # Khi có client kết nối, thêm vào danh sách
        WebSocketServer.clients.add(self)
        print("Client connected")

    def on_close(self):
        # Khi client ngắt kết nối, loại bỏ khỏi danh sách
        WebSocketServer.clients.remove(self)
        print("Client disconnected")

    @classmethod
    def send_message(cls, message: str):
        # Gửi tin nhắn đến tất cả client đang kết nối
        print(f"Sending message '{message}' to {len(cls.clients)} client(s).")
        for client in cls.clients:
            client.write_message(message)

# Lớp chọn từ ngẫu nhiên từ danh sách có sẵn
class RandomWordSelector:
    def __init__(self, word_list):
        self.word_list = word_list  # Danh sách từ để chọn

    def sample(self):
        """Lấy một từ ngẫu nhiên"""
        return random.choice(self.word_list)

def main():
    # Khởi động WebSocket server và gửi từ ngẫu nhiên định kỳ
    app = tornado.web.Application(
        [(r"/websocket/", WebSocketServer)],  # Định tuyến WebSocket
        websocket_ping_interval=10,  # Khoảng thời gian gửi ping
        websocket_ping_timeout=30    # Thời gian chờ phản hồi trước khi ngắt kết nối
    )

    app.listen(8888)  # Lắng nghe trên cổng 8888
    io_loop = tornado.ioloop.IOLoop.current()  # Lấy event loop hiện tại

    word_selector = RandomWordSelector(['apple', 'banana', 'orange', 'grape', 'melon'])
    
    # Định kỳ gửi từ ngẫu nhiên đến client mỗi 3 giây (3000ms)
    periodic_callback = tornado.ioloop.PeriodicCallback(
        lambda: WebSocketServer.send_message(word_selector.sample()), 3000
    )
    periodic_callback.start()

    io_loop.start()  # Chạy event loop

if __name__ == "__main__":
    main()
