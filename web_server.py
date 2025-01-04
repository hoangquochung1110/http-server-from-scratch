import socket
from web_application import application

CRLF = '\r\n'


def parse_header_line(line):
    key, value = line.split(':', maxsplit=1)
    return (format_header_key(key), value.strip())


def parse_request_line(line):
    return line.split()


def format_header_key(key):
    return 'HTTP_' + key.upper().replace('-', '_').replace(' ', '_')


def parse_http(data):
    request_line, *header_lines = data.split(CRLF)
    method, path, protocol = parse_request_line(request_line)
    headers = dict(
        parse_header_line(line)
        for line in header_lines
    )
    return {
        'PATH_INFO': path,
        'REQUEST_METHOD': method,
        'SERVER_PROTOCOL': protocol,
        **headers,
    }



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', 8000))
    s.listen(1)
    print("Server is listening on port 8000...")

    try:
        while True:
            conn, addr = s.accept()
            print(f"Connection from {addr} accepted.")

            try:
                http_request = conn.recv(1024).decode("utf-8").strip()
                environ = parse_http(http_request)

                def start_response(status, headers):
                    conn.sendall(f'HTTP/1.1 {status}{CRLF}'.encode('utf-8'))
                    for key, value in headers:
                        conn.sendall(f'{key}: {value}{CRLF}'.encode('utf-8'))
                    conn.sendall(CRLF.encode('utf-8'))

                response = application(start_response, environ)
                for data in response:
                    conn.sendall(data.encode("utf-8"))

            except Exception as e:
                print(f"Error handling request: {e}")

            finally:
                conn.close()  # Ensure connection is closed

    except KeyboardInterrupt:
        print("\nServer is shutting down gracefully...")

