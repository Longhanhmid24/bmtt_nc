import socket

def hand_request(client_socket, request_data):
    if "GET /admin" in request_data:  # Sửa "GET/ admin" thành "GET /admin"
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"  # Sửa "Context-type" thành "Content-Type"
        with open("admin.html", "r") as file:
            response += file.read()
    else:
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"  # Sửa "Context-type" thành "Content-Type"
        with open("index.html", "r") as file:
            response += file.read()
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)

    print("Listening on port 8080...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        request_data = client_socket.recv(1024).decode('utf-8')
        print(f"Request data: {request_data}")  # Thêm log để kiểm tra request
        hand_request(client_socket, request_data)

if __name__ == '__main__':
    main()