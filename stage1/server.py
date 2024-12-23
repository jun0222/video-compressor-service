# tcpでクライアントからの接続を待ち受ける
import socket

def start_server(host="0.0.0.0", port=12345):
    # ソケットを作成
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # アドレスとポートをバインド
        server_socket.bind((host, port))

        # 接続の待ち受け（最大5接続）
        server_socket.listen(5)
        print(f"Server started on {host}:{port}")

        while True:
            print("Waiting for a connection...")

            # クライアントからの接続を受け入れ
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            # クライアントからのデータを受信
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Received: {data}")

            # 応答を送信
            response = "Message received"
            client_socket.sendall(response.encode('utf-8'))

            # 接続を閉じる
            client_socket.close()
            print(f"Connection with {client_address} closed")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # サーバーソケットを閉じる
        server_socket.close()
        print("Server stopped")

if __name__ == "__main__":
    start_server()

## 細かい情報
# クライアントから受け取ったデータをmp4として処理する。他の形式は弾く
## 細かい情報