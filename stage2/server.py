# server.py
import socket
import os
import subprocess

def save_file(file_data, file_name="uploaded_file.mp4"):
    """Save uploaded file to disk"""
    with open(file_name, "wb") as f:
        f.write(file_data)
    print(f"File saved as {file_name}")

def convert_to_gif_or_webp(input_file, output_file, start_time, duration, output_format):
    """Convert video to gif or webp using FFmpeg"""
    try:
        # FFmpeg conversion command
        command = [
            "ffmpeg", "-i", input_file, "-ss", start_time, "-t", duration,
            "-vf", "fps=10,scale=320:-1", "-y", output_file
        ]
        if output_format == "gif":
            command.append("-f")
            command.append("gif")
        elif output_format == "webp":
            command.extend(["-vcodec", "libwebp"])
        else:
            print(f"Unsupported format: {output_format}")
            return None

        subprocess.run(command, check=True)
        print(f"Converted successfully: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error converting to {output_format}: {e}")
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

            # Receive metadata (file size, start_time, duration, output_format)
            metadata_bytes = client_socket.recv(96)
            file_size = int(metadata_bytes[:32].decode('utf-8').strip())
            start_time = metadata_bytes[32:48].decode('utf-8').strip()
            duration = metadata_bytes[48:64].decode('utf-8').strip()
            output_format = metadata_bytes[64:96].decode('utf-8').strip()
            print(f"File size: {file_size}, Start time: {start_time}, Duration: {duration}, Format: {output_format}")

            # Receive file data
            received_data = b""
            while len(received_data) < file_size:
                chunk = client_socket.recv(1400)
                if not chunk:
                    break
                received_data += chunk

            uploaded_file = "uploaded_file.mp4"
            output_file = f"output.{output_format}"

            # Save the uploaded file
            save_file(received_data, uploaded_file)

            # Convert to gif or webp
            converted_file_path = convert_to_gif_or_webp(uploaded_file, output_file, start_time, duration, output_format)

            if converted_file_path and os.path.isfile(converted_file_path):
                converted_size = os.path.getsize(converted_file_path)
                client_socket.sendall(f"{converted_size:>32}".encode('utf-8'))

                with open(converted_file_path, "rb") as f:
                    while chunk := f.read(1400):
                        client_socket.sendall(chunk)
                print(f"{output_format.upper()} file sent successfully")
            else:
                client_socket.sendall(f"{0:>32}".encode('utf-8'))
                print(f"Failed to convert to {output_format.upper()}")

            client_socket.close()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server_socket.close()
        print("Server stopped")

if __name__ == "__main__":
    start_server()
