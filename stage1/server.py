# server.py
import socket
import struct

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

            # 最初の32バイトでファイルサイズを受信
            file_size_bytes = client_socket.recv(32)
            if len(file_size_bytes) < 32:
                print("Failed to receive file size")
                client_socket.close()
                continue

            # 32バイトを文字列として解釈し、整数に変換
            file_size_str = file_size_bytes.decode('utf-8').strip()
            file_size = int(file_size_str)
            print(f"File size received: {file_size} bytes")

            # ファイルデータの受信
            received_data = b""
            while len(received_data) < file_size:
                chunk = client_socket.recv(1400)
                if not chunk:
                    break
                received_data += chunk

            print(f"Received file data: {received_data[:50]}... (truncated)")

            # 応答を送信
            response = "File size and data received successfully"
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