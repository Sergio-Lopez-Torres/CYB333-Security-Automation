"""CYB333 Part 2: small, permission-limited TCP connect port scanner."""
import argparse
import ipaddress
import socket
import time

ALLOWED_HOSTS = {'localhost', '127.0.0.1', 'scanme.nmap.org'}


def port_number(value):
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError('Port must be an integer.') from error
    if not 1 <= number <= 65535:
        raise argparse.ArgumentTypeError('Port must be between 1 and 65535.')
    return number


def scan(host, start, end):
    if host not in ALLOWED_HOSTS:
        raise ValueError('Only localhost, 127.0.0.1, and scanme.nmap.org are authorized.')
    if end < start:
        raise ValueError('End port must be greater than or equal to start port.')
    try:
        address = socket.gethostbyname(host)
    except socket.gaierror as error:
        raise ValueError(f'Cannot resolve host {host}: {error}') from error
    if host == 'scanme.nmap.org' and ipaddress.ip_address(address).is_private:
        raise ValueError('Unexpected private address for scanme.nmap.org; refusing to scan.')
    print(f'Scanning {host} ({address}), ports {start}-{end}')
    started = time.monotonic()
    for port in range(start, end + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                code = sock.connect_ex((address, port))
            status = 'OPEN' if code == 0 else 'CLOSED/UNREACHABLE'
        except OSError as error:
            status = f'ERROR ({error})'
        print(f'Port {port:5d}: {status}')
        # Keep external testing gentle and limited.
        if host == 'scanme.nmap.org':
            time.sleep(0.2)
    print(f'Finished in {time.monotonic() - started:.2f} seconds.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('host', help='127.0.0.1, localhost, or scanme.nmap.org')
    parser.add_argument('start_port', type=port_number)
    parser.add_argument('end_port', type=port_number)
    args = parser.parse_args()
    try:
        scan(args.host.lower(), args.start_port, args.end_port)
    except ValueError as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
