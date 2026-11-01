import socket
import ssl

# Server configuration
serverIP = '192.168.1.87'
serverPort = 12000

def main():
    # Create a regular TCP socket
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # For self-signed certs

    # Wrap the raw socket with TLS
    tls_socket = context.wrap_socket(raw_socket, server_hostname=serverIP)

    try:
        # Connect (TLS handshake happens here)
        print(f"[TLS CLIENT] Connecting to {serverIP}:{serverPort}...")
        tls_socket.connect((serverIP, serverPort))
        print("[TLS CLIENT] TLS handshake complete!")

        # Get user input
        message = input('Input lowercase sentence: ')

        # Send the message (encrypted)
        tls_socket.send(message.encode())
        print(f"[TLS CLIENT] Sent: {message}")

        # Receive the reply (encrypted)
        response = tls_socket.recv(1024).decode()
        print(f"[TLS SERVER] {response}")

    except Exception as e:
        print(f"[TLS CLIENT] Error: {e}")
    finally:
        tls_socket.close()
        print("[TLS CLIENT] Connection closed")

if __name__ == '__main__':
    main()