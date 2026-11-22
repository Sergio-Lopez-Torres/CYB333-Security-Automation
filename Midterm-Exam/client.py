"""CYB333 Part 1: local TCP client."""
import socket

HOST = '127.0.0.1'
PORT = 5000


def main():
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as client:
            print(f'Connected to server at {HOST}:{PORT}')
            message = 'Hello from the CYB333 client!'
            client.sendall(message.encode('utf-8'))
            print(f'Sent to server: {message}')
            response = client.recv(1024)
            if response:
                print(f'Received from server: {response.decode("utf-8", errors="replace")}')
            else:
                print('Server closed without a response.')
        print('Client disconnected cleanly.')
    except ConnectionRefusedError:
        print('Connection refused: start server.py before running the client.')
    except socket.timeout:
        print('Connection timed out.')
    except OSError as error:
        print(f'Connection error: {error}')


if __name__ == '__main__':
    main()
