import socket
import ssl

# Server configuration
serverIP = '0.0.0.0'
serverPort = 12000

# Certificate files
CERT_FILE = '/home/satwal/cmpn3000/certs/server.crt'
KEY_FILE = '/home/satwal/cmpn3000/certs/server.key'

def main():
    # Create a regular TCP socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((serverIP, serverPort))
    serverSocket.listen(1)

    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    print(f"[TLS SERVER] Listening on port {serverPort}...")

    while True:
        try:
            # Accept a raw TCP connection
            raw_socket, clientAddress = serverSocket.accept()
            print(f"[TLS SERVER] Raw connection from {clientAddress}")

            # Wrap the raw socket with TLS
            tls_socket = context.wrap_socket(raw_socket, server_side=True)
            print(f"[TLS SERVER] TLS handshake complete with {clientAddress}")

            # Receive the message
            message = tls_socket.recv(1024).decode()
            print(f"[TLS SERVER] Received: {message}")

            # Process and send back
            response = message.upper()
            tls_socket.send(response.encode())
            print(f"[TLS SERVER] Sent back: {response}")

            # Close the TLS connection
            tls_socket.close()

        except KeyboardInterrupt:
            print("\n[TLS SERVER] Shutting down...")
            break
        except Exception as e:
            print(f"[TLS SERVER] Error: {e}")

    serverSocket.close()

if __name__ == '__main__':
    main()
