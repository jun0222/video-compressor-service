# client.py
import socket
import struct
import os

def start_client(file_path, host="127.0.0.1", port=12345):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # サーバーに接続
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # ファイルサイズを取得
        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size} bytes")

        # ファイルサイズを32バイトの文字列で送信（右詰めパディング）
        file_size_str = f"{file_size:>32}"
        client_socket.sendall(file_size_str.encode('utf-8'))

        # ファイルデータを送信
        with open(file_path, "rb") as f:
            while chunk := f.read(1400):
                client_socket.sendall(chunk)

        # サーバーからの応答を受信（16バイトのステータス情報）
        response = client_socket.recv(16).decode('utf-8').strip()
        print(f"Server response: {response}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    # アップロードする動画ファイルのパスを指定
    file_path = "video.mp4"  # 必要に応じて変更
    start_client(file_path)