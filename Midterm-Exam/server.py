"""CYB333 Part 1: local TCP echo server."""
import socket

HOST = '127.0.0.1'
PORT = 5000


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(1)
            print(f'Server listening on {HOST}:{PORT}', flush=True)
            connection, address = server.accept()
            with connection:
                print(f'Client connected: {address}', flush=True)
                connection.settimeout(15)
                while True:
                    try:
                        data = connection.recv(1024)
                    except socket.timeout:
                        print('Client inactive; closing connection.', flush=True)
                        break
                    if not data:
                        print('Client disconnected cleanly.', flush=True)
                        break
                    message = data.decode('utf-8', errors='replace')
                    print(f'Received from client: {message}', flush=True)
                    response = f'Server received: {message}'
                    connection.sendall(response.encode('utf-8'))
                    print(f'Sent to client: {response}', flush=True)
    except (OSError, KeyboardInterrupt) as error:
        print(f'Server stopped or failed: {error}', flush=True)
    finally:
        print('Server shutdown complete.', flush=True)


if __name__ == '__main__':
    main()
