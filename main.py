import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import socket
import logging
from threading import Thread
from datetime import datetime


MAIN_DIR = pathlib.Path()
UDP_IP = '127.0.0.1'
UDP_PORT = 5000
MESSAGE = "Python Web development"


def send_data_to_socket(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(data, (UDP_IP, UDP_PORT))
    client_socket.close()


class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message.html':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        send_data_to_socket(data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('0.0.0.0', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def run_socket_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            save_data_from_html_server(data)
            print(f'Received data: {data.decode()} from: {address}')
            sock.sendto(data, address)
            print(f'Send data: {data.decode()} to: {address}')

    except KeyboardInterrupt:
        logging.info('Destroy server')
    finally:
        sock.close()


def save_data_from_html_server(data):
    data_parse = urllib.parse.unquote_plus(data.decode())
    try:
        #uid = str(uuid4())
        data_dict = {str(datetime.now()): {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}}

        with open('storage/data.json', 'r+') as fd:
            data = json.load(fd)

        data.update(data_dict)

        with open('storage/data.json', 'w', encoding='utf-8') as fd:
            json.dump(data, fd, ensure_ascii=False, indent=4)

    except ValueError as err:
        logging.exception(f"Failed to parse data {data_parse}: {err}")

    except OSError as err:
        logging.exception(f"Failed to write data {data_parse}: {err}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

    STORAGE_DIR = pathlib.Path().joinpath('data')
    FILE_STORAGE = STORAGE_DIR / 'data.json'
    if not FILE_STORAGE.exists():
        with open('storage/data.json', 'w', encoding='utf-8') as fd:
            json.dump({}, fd, ensure_ascii=False, indent=4)

    th_server = Thread(target=run)
    th_server.start()

    th_socket_server = Thread(target=run_socket_server, args=(UDP_IP, UDP_PORT))
    th_socket_server.start()
