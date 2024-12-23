import socket

def start_client(host="127.0.0.1", port=12345):
    # ソケットを作成
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # サーバーに接続
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # サーバーにメッセージを送信
        message = "Hello, Server!"
        print(f"Sending: {message}")
        client_socket.sendall(message.encode('utf-8'))

        # サーバーからの応答を受信
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Received: {response}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # ソケットを閉じる
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    start_client()