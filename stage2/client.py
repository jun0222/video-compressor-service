# client.py
import socket
import os

def start_client(file_path, start_time, duration, output_format, host="127.0.0.1", port=12345):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size} bytes")

        start_time_str = f"{start_time}".ljust(16)
        duration_str = f"{duration}".ljust(16)
        output_format_str = f"{output_format}".ljust(32)

        # Send metadata
        metadata = f"{file_size:>32}".encode('utf-8') + start_time_str.encode('utf-8') + duration_str.encode('utf-8') + output_format_str.encode('utf-8')
        client_socket.sendall(metadata)

        # Send file data
        with open(file_path, "rb") as f:
            while chunk := f.read(1400):
                client_socket.sendall(chunk)

        # Receive converted file size
        converted_size_bytes = client_socket.recv(32)
        converted_size = int(converted_size_bytes.decode('utf-8').strip())

        if converted_size > 0:
            print(f"Converted file size: {converted_size} bytes")

            # Receive converted file data
            converted_data = b""
            while len(converted_data) < converted_size:
                chunk = client_socket.recv(1400)
                if not chunk:
                    break
                converted_data += chunk

            # Save converted file
            converted_file_path = f"output.{output_format}"
            with open(converted_file_path, "wb") as f:
                f.write(converted_data)
            print(f"Converted file saved as: {converted_file_path}")
        else:
            print(f"Failed to convert file to {output_format.upper()}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    file_path = "video.mp4"  # Replace with your video file path
    start_time = "00:00:03"  # Start time for conversion
    duration = "5"           # Duration in seconds
    output_format = "webp"    # Output format: 'gif' or 'webp'
    start_client(file_path, start_time, duration, output_format)
