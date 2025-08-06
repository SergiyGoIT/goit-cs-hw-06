import socket
import os
from datetime import datetime
from urllib.parse import unquote_plus

HOST = '127.0.0.1'
PORT = 3000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

def parse_request(request):
    try:
        lines = request.splitlines()
        method, path, _ = lines[0].split()
        return method, path
    except Exception:
        return None, None

def load_file(path, binary=False):
    mode = 'rb' if binary else 'r'
    try:
        with open(path, mode) as f:
            return f.read()
    except FileNotFoundError:
        return None

def handle_static(path):
    filepath = os.path.join(STATIC_DIR, path.replace('/static/', ''))
    content = load_file(filepath, binary=True)
    if content:
        return b"HTTP/1.1 200 OK\r\n\r\n" + content
    return serve_404()

def serve_404():
    content = load_file(os.path.join(TEMPLATE_DIR, "error.html"))
    return f"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n{content}".encode()

def build_response(content, status="200 OK"):
    return f"HTTP/1.1 {status}\r\nContent-Type: text/html\r\n\r\n{content}".encode()

def save_message(data):
    # Підготовка до передачі сокет-серверу (буде у наступному кроці)
    import socket as sock
    client = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    client.sendto(data.encode(), ('127.0.0.1', 5000))
    client.close()

def handle_post(body):
    data = {}
    for pair in body.split('&'):
        key, value = pair.split('=')
        data[key] = unquote_plus(value)
    data['date'] = str(datetime.now())
    save_message(str(data))  # передаємо в сокет-сервер
    return load_file(os.path.join(TEMPLATE_DIR, "index.html"))

def run_http_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"HTTP Server running at http://{HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            with conn:
                request = conn.recv(1024).decode()
                method, path = parse_request(request)
                print(f"Request: {method} {path}")

                if method == 'GET':
                    if path == '/':
                        content = load_file(os.path.join(TEMPLATE_DIR, "index.html"))
                        response = build_response(content)
                    elif path == '/message':
                        content = load_file(os.path.join(TEMPLATE_DIR, "message.html"))
                        response = build_response(content)
                    elif path.startswith('/static/'):
                        response = handle_static(path)
                    else:
                        response = serve_404()

                elif method == 'POST':
                    body = request.split("\r\n\r\n", 1)[1]
                    content = handle_post(body)
                    response = build_response(content)

                else:
                    response = serve_404()

                conn.sendall(response)
