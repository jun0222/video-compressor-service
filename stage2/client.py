# client.py
import socket
import os

def start_client(file_path, host="127.0.0.1", port=12345):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size} bytes")

        # Send file size
        file_size_str = f"{file_size:>32}".encode('utf-8')
        client_socket.sendall(file_size_str)

        # Send file data
        with open(file_path, "rb") as f:
            while chunk := f.read(1400):
                client_socket.sendall(chunk)

        # Receive audio file size
        audio_size_bytes = client_socket.recv(32)
        audio_size = int(audio_size_bytes.decode('utf-8').strip())
        print(f"Audio file size: {audio_size} bytes")

        # Receive audio file data
        audio_data = b""
        while len(audio_data) < audio_size:
            chunk = client_socket.recv(1400)
            if not chunk:
                break
            audio_data += chunk

        # Save audio file
        audio_file_path = "audio_" + os.path.splitext(os.path.basename(file_path))[0] + ".mp3"
        with open(audio_file_path, "wb") as f:
            f.write(audio_data)
        print(f"Audio file saved as: {audio_file_path}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    file_path = "video.mp4"  # Replace with the path to your video file
    start_client(file_path)
