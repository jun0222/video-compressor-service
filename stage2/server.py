# server.py
import socket
import struct
import os
import subprocess

def save_file(file_data, file_name="uploaded_file.mp4"):
    """指定された名前でファイルを保存"""
    with open(file_name, "wb") as f:
        f.write(file_data)
    print(f"File saved as {file_name}")

def compress_video(input_file, output_file, bitrate="1M"):
    """FFmpegを使用して動画を圧縮"""
    try:
        command = [
            "ffmpeg", "-i", input_file, "-b:v", bitrate, "-y", output_file
        ]
        subprocess.run(command, check=True)
        print(f"Video compressed successfully: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error compressing video: {e}")
        return None

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

            # MP4ファイルのヘッダーを確認（'ftyp'ボックスを検出）
            if received_data[:12].find(b'ftyp') != -1:
                print("MP4 file confirmed")
                uploaded_file = "uploaded_file.mp4"
                compressed_file = "compressed_file.mp4"

                # ファイル保存
                save_file(received_data, uploaded_file)

                # 圧縮処理
                compressed_file_path = compress_video(uploaded_file, compressed_file)

                if compressed_file_path and os.path.isfile(compressed_file_path):
                    # 圧縮後のファイルをクライアントに送信
                    compressed_size = os.path.getsize(compressed_file_path)
                    print(f"Compressed file size: {compressed_size} bytes")

                    # 圧縮ファイルサイズを送信
                    compressed_size_str = f"{compressed_size:>32}"
                    client_socket.sendall(compressed_size_str.encode('utf-8'))

                    # 圧縮ファイルデータを送信
                    with open(compressed_file_path, "rb") as f:
                        while chunk := f.read(1400):
                            client_socket.sendall(chunk)

                    print("Compressed file sent successfully")
                else:
                    print("Compression failed")
                    status_message = "Compression failed".ljust(16).encode('utf-8')
                    client_socket.sendall(status_message)
            else:
                print("Not an MP4 file")
                status_message = "Invalid format".ljust(16).encode('utf-8')
                client_socket.sendall(status_message)

            client_socket.close()
            print(f"Connection with {client_address} closed")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server_socket.close()
        print("Server stopped")

if __name__ == "__main__":
    start_server()
