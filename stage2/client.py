# client.py
import socket
import os

def start_client(file_path, start_time, duration, output_format, resolution=None, aspect_ratio=None, host="127.0.0.1", port=12345):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size} bytes")

        # Prepare metadata
        start_time_str = f"{start_time}".ljust(16)
        duration_str = f"{duration}".ljust(16)
        output_format_str = f"{output_format}".ljust(32)
        resolution_str = f"{resolution}".ljust(32) if resolution else "".ljust(32)
        aspect_ratio_str = f"{aspect_ratio}".ljust(32) if aspect_ratio else "".ljust(32)

        metadata = (
            f"{file_size:>32}".encode('utf-8') +
            start_time_str.encode('utf-8') +
            duration_str.encode('utf-8') +
            output_format_str.encode('utf-8') +
            resolution_str.encode('utf-8') +
            aspect_ratio_str.encode('utf-8')
        )
        print("Metadata being sent to server:")
        print(f"File size: {file_size}, Start time: {start_time}, Duration: {duration}, Format: {output_format}, Resolution: {resolution}, Aspect Ratio: {aspect_ratio}")

        # Send metadata
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
            base_name, _ = os.path.splitext(os.path.basename(file_path))
            converted_file_path = f"{base_name}_converted.{output_format}"
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
    output_format = "mp4"    # Output format: 'mp4', 'gif', 'webp', etc.
    resolution = "640x360"   # Example resolution
    aspect_ratio = "16:9"    # Example aspect ratio
    start_client(file_path, start_time, duration, output_format, resolution, aspect_ratio)
