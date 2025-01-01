# client.py
import socket
import os

def start_client(file_path, start_time, duration, output_format, resolution=None, aspect_ratio=None, host="127.0.0.1", port=12345):
    # ファイルが存在するか確認
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    # ソケットを作成し、サーバーに接続
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # サーバーへの接続を確立
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # アップロードするファイルのサイズを取得
        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size} bytes")

        # メタデータを準備
        start_time_str = f"{start_time}".ljust(16)  # 開始時刻
        duration_str = f"{duration}".ljust(16)      # 継続時間
        output_format_str = f"{output_format}".ljust(32)  # 出力フォーマット
        resolution_str = f"{resolution}".ljust(32) if resolution else "".ljust(32)  # 解像度
        aspect_ratio_str = f"{aspect_ratio}".ljust(32) if aspect_ratio else "".ljust(32)  # アスペクト比

        # メタデータを1つのバイト列にまとめて送信
        metadata = (
            f"{file_size:>32}".encode('utf-8') +  # ファイルサイズを32バイトに整形
            start_time_str.encode('utf-8') +
            duration_str.encode('utf-8') +
            output_format_str.encode('utf-8') +
            resolution_str.encode('utf-8') +
            aspect_ratio_str.encode('utf-8')
        )
        print("Metadata being sent to server:")
        print(f"File size: {file_size}, Start time: {start_time}, Duration: {duration}, Format: {output_format}, Resolution: {resolution}, Aspect Ratio: {aspect_ratio}")

        # メタデータをサーバーに送信
        client_socket.sendall(metadata)

        # ファイルデータをチャンク単位で送信
        with open(file_path, "rb") as f:
            while chunk := f.read(1400):  # 1400バイトずつ読み取る
                client_socket.sendall(chunk)

        # サーバーから変換後のファイルサイズを受信
        converted_size_bytes = client_socket.recv(32)
        converted_size = int(converted_size_bytes.decode('utf-8').strip())  # バイト列を整数に変換

        if converted_size > 0:
            print(f"Converted file size: {converted_size} bytes")

            # 変換後のファイルデータを受信
            converted_data = b""
            while len(converted_data) < converted_size:
                chunk = client_socket.recv(1400)  # 1400バイトずつ受信
                if not chunk:
                    break
                converted_data += chunk

            # 変換後のファイルを保存
            base_name, _ = os.path.splitext(os.path.basename(file_path))  # 元ファイル名の拡張子を除去
            converted_file_path = f"{base_name}_converted.{output_format}"  # 出力ファイル名を生成
            with open(converted_file_path, "wb") as f:
                f.write(converted_data)
            print(f"Converted file saved as: {converted_file_path}")
        else:
            print(f"Failed to convert file to {output_format.upper()}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # ソケットを閉じる
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    # 実行時に必要な情報を指定
    file_path = "video.mp4"  # 入力ファイルのパス
    start_time = "00:00:03"  # 変換開始時刻
    duration = "5"           # 変換する動画の継続時間（秒）
    output_format = "mp4"    # 出力フォーマット
    resolution = "640x360"   # 出力解像度
    aspect_ratio = "16:9"    # 出力アスペクト比
    start_client(file_path, start_time, duration, output_format, resolution, aspect_ratio)
