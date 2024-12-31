# server.py
import socket
import os
import subprocess

def save_file(file_data, file_name="uploaded_file.mp4"):
    """Save uploaded file to disk"""
    with open(file_name, "wb") as f:
        f.write(file_data)
    print(f"File saved as {file_name}")

def convert_to_audio(input_file, output_file):
    """Convert video to audio using FFmpeg"""
    try:
        # Check for audio stream
        result = subprocess.run(["ffmpeg", "-i", input_file], stderr=subprocess.PIPE, text=True)
        print("FFmpeg input analysis:\n", result.stderr)  # Log FFmpeg analysis
        if "Audio" not in result.stderr:
            print("No audio stream found in the input file.")
            return None

        # Convert to audio
        command = ["ffmpeg", "-i", input_file, "-vn", "-q:a", "0", "-y", output_file]
        subprocess.run(command, check=True)
        print(f"Audio extracted successfully: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error converting to audio: {e}")
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

            # Receive file size
            file_size_bytes = client_socket.recv(32)
            if not file_size_bytes.strip():
                print("Failed to receive file size")
                client_socket.close()
                continue

            file_size = int(file_size_bytes.decode('utf-8').strip())
            print(f"File size: {file_size} bytes")

            # Receive file data
            received_data = b""
            while len(received_data) < file_size:
                chunk = client_socket.recv(1400)
                if not chunk:
                    break
                received_data += chunk

            uploaded_file = "uploaded_file.mp4"
            audio_file = "audio_file.mp3"

            # Save the uploaded file
            save_file(received_data, uploaded_file)

            # Convert to audio
            audio_file_path = convert_to_audio(uploaded_file, audio_file)

            if audio_file_path and os.path.isfile(audio_file_path):
                audio_size = os.path.getsize(audio_file_path)
                print(f"Audio file size: {audio_size} bytes")
                client_socket.sendall(f"{audio_size:>32}".encode('utf-8'))
                print("Sent audio file size to client")

                with open(audio_file_path, "rb") as f:
                    while chunk := f.read(1400):
                        client_socket.sendall(chunk)
                print("Audio file sent successfully")

            client_socket.close()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server_socket.close()
        print("Server stopped")

if __name__ == "__main__":
    start_server()
