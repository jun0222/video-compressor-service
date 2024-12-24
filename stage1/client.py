# client.py
import socket

def start_client(host="127.0.0.1", port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # サーバーに接続
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # ファイルデータを準備
        file_data = "Hello, Server! " * 100  # 模擬的なファイルデータ
        file_size = len(file_data.encode('utf-8'))
        print(f"File size: {file_size} bytes")

        # ファイルサイズを32バイトの文字列で送信（右詰めパディング）
        file_size_str = f"{file_size:>32}"
        client_socket.sendall(file_size_str.encode('utf-8'))

        # ファイルデータを送信
        client_socket.sendall(file_data.encode('utf-8'))

        # サーバーからの応答を受信
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Received: {response}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    start_client()
