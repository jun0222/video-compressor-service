# client.py
import socket
import os

def start_client(file_path, resolution=None, aspect_ratio=None, host="127.0.0.1", port=12345):
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

        # 解像度を32バイト、アスペクト比を16バイトで準備（空の場合はパディング）
        resolution_str = f"{resolution}".ljust(32) if resolution else "".ljust(32)
        aspect_ratio_str = f"{aspect_ratio}".ljust(16) if aspect_ratio else "".ljust(16)

        # メタデータ（ファイルサイズ + 解像度 + アスペクト比）を送信
        metadata = f"{file_size:>32}".encode('utf-8') + resolution_str.encode('utf-8') + aspect_ratio_str.encode('utf-8')
        client_socket.sendall(metadata)

        # ファイルデータを送信
        with open(file_path, "rb") as f:
            while chunk := f.read(1400):
                client_socket.sendall(chunk)

        # サーバーからの圧縮ファイルサイズを受信
        compressed_size_bytes = client_socket.recv(32)
        compressed_size = int(compressed_size_bytes.decode('utf-8').strip())
        print(f"Compressed file size: {compressed_size} bytes")

        # 圧縮ファイルデータを受信
        compressed_data = b""
        while len(compressed_data) < compressed_size:
            chunk = client_socket.recv(1400)
            if not chunk:
                break
            compressed_data += chunk

        # 圧縮ファイルを保存
        compressed_file_path = "compressed_" + os.path.basename(file_path)
        with open(compressed_file_path, "wb") as f:
            f.write(compressed_data)
        print(f"Compressed file saved as: {compressed_file_path}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    # アップロードする動画ファイルのパスを指定
    file_path = "video.mp4"  # 必要に応じて変更
    resolution = "1280x720"  # 圧縮解像度を指定（例: "1280x720", "640x480" など）
    aspect_ratio = "4:3"   # アスペクト比を指定（例: "16:9", "4:3"）
    start_client(file_path, resolution, aspect_ratio)
