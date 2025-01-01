# server.py
import socket
import os
import subprocess

def save_file(file_data, file_name="uploaded_file.mp4"):
    """受信したファイルデータを保存"""
    with open(file_name, "wb") as f:
        f.write(file_data)
    print(f"File saved as {file_name}")

def convert_video(input_file, output_file, start_time, duration, resolution=None, aspect_ratio=None):
    """指定された条件で動画を変換"""
    try:
        # FFmpegの基本コマンド
        command = [
            "ffmpeg", "-i", input_file, "-ss", start_time, "-t", duration
        ]

        # 解像度とアスペクト比が指定されている場合に追加
        if resolution or aspect_ratio:
            video_filters = []
            if resolution:
                video_filters.append(f"scale={resolution}")  # 解像度を指定
            if video_filters:
                command.extend(["-vf", ",".join(video_filters)])  # -vfオプションに追加
            if aspect_ratio:
                command.extend(["-aspect", aspect_ratio])  # アスペクト比を指定

        # エンコード設定を追加
        command.extend(["-c:v", "libx264", "-preset", "fast", "-crf", "23", "-y", output_file])

        # 実行するFFmpegコマンドをログに出力
        print(f"Running FFmpeg command: {' '.join(command)}")

        # コマンドを実行
        subprocess.run(command, check=True)
        print(f"Video converted successfully: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error converting video: {e}")
        return None

def start_server(host="0.0.0.0", port=12345):
    """サーバーを起動してクライアントからの接続を待つ"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # ソケットをバインドしてリスニング状態にする
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server started on {host}:{port}")

        while True:
            print("Waiting for a connection...")
            client_socket, client_address = server_socket.accept()  # クライアントからの接続を受け入れる
            print(f"Connection from {client_address}")

            # メタデータ（ファイルサイズ、開始時刻、継続時間など）を受信
            metadata_bytes = client_socket.recv(160)  # メタデータは160バイト
            file_size = int(metadata_bytes[:32].decode('utf-8').strip())  # ファイルサイズを整数に変換
            start_time = metadata_bytes[32:48].decode('utf-8').strip()  # 開始時刻
            duration = metadata_bytes[48:64].decode('utf-8').strip()  # 継続時間
            output_format = metadata_bytes[64:96].decode('utf-8').strip()  # 出力フォーマット
            resolution = metadata_bytes[96:128].decode('utf-8').strip() or None  # 解像度
            aspect_ratio = metadata_bytes[128:160].decode('utf-8').strip() or None  # アスペクト比
            print(f"File size: {file_size}, Start time: {start_time}, Duration: {duration}, Format: {output_format}, Resolution: {resolution}, Aspect Ratio: {aspect_ratio}")

            # ファイルデータを受信
            received_data = b""
            while len(received_data) < file_size:
                chunk = client_socket.recv(1400)  # 1400バイトずつ受信
                if not chunk:
                    break
                received_data += chunk

            # 受信したファイルを保存
            uploaded_file = "uploaded_file.mp4"
            output_file = f"output.{output_format}"  # 出力ファイル名を生成
            save_file(received_data, uploaded_file)

            # ファイルを変換
            converted_file_path = convert_video(
                uploaded_file, output_file, start_time, duration, resolution, aspect_ratio
            )

            # 変換結果をクライアントに送信
            if converted_file_path and os.path.isfile(converted_file_path):
                converted_size = os.path.getsize(converted_file_path)  # 変換後のファイルサイズを取得
                client_socket.sendall(f"{converted_size:>32}".encode('utf-8'))  # ファイルサイズを送信

                # ファイルデータを送信
                with open(converted_file_path, "rb") as f:
                    while chunk := f.read(1400):  # 1400バイトずつ送信
                        client_socket.sendall(chunk)
                print(f"{output_format.upper()} file sent successfully")
            else:
                # 変換が失敗した場合はサイズ0を送信
                client_socket.sendall(f"{0:>32}".encode('utf-8'))
                print(f"Failed to convert to {output_format.upper()}")

            client_socket.close()  # クライアントとの接続を閉じる

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # サーバーを停止
        server_socket.close()
        print("Server stopped")

if __name__ == "__main__":
    # サーバーを起動
    start_server()
