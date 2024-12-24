import socket

def send_in_chunks(socket, data, chunk_size=1400, end_marker="<END>"):
    """データをチャンクに分割して送信し、終了マーカーを送信"""
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        socket.sendall(chunk.encode('utf-8'))
    # 終了マーカーを送信
    socket.sendall(end_marker.encode('utf-8'))

def start_client(host="127.0.0.1", port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # サーバーに接続
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # 送信するデータを準備
        message = "Hello, Server! " * 100  # 長いメッセージ
        print(f"Sending data in chunks of 1400 bytes...")

        # データをチャンクに分割して送信
        send_in_chunks(client_socket, message)

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
