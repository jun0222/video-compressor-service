import socket

def receive_all(client_socket, buffer_size=1400, end_marker="<END>"):
    """全データを受信し、終了マーカーが見つかるまでデータを受信"""
    data = ""
    while True:
        part = client_socket.recv(buffer_size).decode('utf-8')
        if end_marker in part:  # 終了マーカーを検出
            data += part.replace(end_marker, "")  # マーカーを除去して保存
            break
        data += part
    return data

def start_server(host="0.0.0.0", port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server started on {host}:{port}")

        while True:
            print("Waiting for a connection...")
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            # データを受信
            data = receive_all(client_socket)
            print(f"Received: {data}")

            # 応答を送信
            response = "Message received"
            client_socket.sendall(response.encode('utf-8'))

            client_socket.close()
            print(f"Connection with {client_address} closed")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server_socket.close()
        print("Server stopped")

if __name__ == "__main__":
    start_server()
