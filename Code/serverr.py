import sys
import socket
import ssl
from Code.http_parser import parse_request
import datetime
import os


class HTTPServer:
    STATUS = {
        200: "OK",
        201: "CREATED",
        400: "BAD REQUEST",
        403: "FORBIDDEN",
        404: "NOT FOUND",
        411: "LENGTH REQUIRED",
        500: "INTERNAL SERVER ERROR",
        501: "NOT IMPLEMENTED",
        505: "HTTP VERSION NOT SUPPORTED"
    }

    def __init__(self):
        if not (3 <= len(sys.argv) <= 5):
            print("Usage: python serverr.py <host> <port> [<cert_file> <key_file>]")
            sys.exit(1)

        self.host = sys.argv[1]
        self.port = int(sys.argv[2])
        self.cert_file = sys.argv[3] if len(sys.argv) >= 4 else None
        self.key_file = sys.argv[4] if len(sys.argv) == 5 else None
        self.is_https = self.cert_file and self.key_file

        if self.cert_file and not self.key_file:
            print("Private key file must be provided with certificate file.")
            sys.exit(1)

        self.start_server()

    def send_response(self, connection, status_code, content="", headers=None):
        if headers is None:
            headers = {}
        status_message = self.STATUS.get(status_code, "UNKNOWN STATUS")
        response = f"HTTP/1.1 {status_code} {status_message}\r\n"
        for header, value in headers.items():
            response += f"{header}: {value}\r\n"
        response += f"Content-Length: {len(content)}\r\n"
        response += "Content-Type: text/plain\r\n\r\n"
        response += content
        connection.sendall(response.encode('iso-8859-1'))

    def logger(self, request_line):
        timestamp = datetime.datetime.now()
        server_log = f"[{timestamp}] {request_line}"
        with open('server.log', 'a') as log_file:
            log_file.write(server_log + "\n")

    def handle_request(self, connection, request):
        print(f"[INFO]  {'HTTPS' if self.use_https else 'HTTP'} connection from {addr}\n")
        try:
            request_details = parse_request(request)
            if len(request_details) == 1:
                response_data = self.build_error_response(request_details[0])
                connection.sendall(response_data)
                connection.close()
                return

            method, uri, http_version, headers, body = request_details if len(request_details) == 4 else request_details + (None, None, None)
            self.logger(f"{method} {uri} {http_version}")
            absolute_path = os.path.join(os.getcwd(), uri.lstrip('/'))

            if not os.path.isfile(absolute_path):
                response_data = self.build_error_response(404)
                connection.sendall(response_data)
                connection.close()
                return

            if method == 'GET':
                self.handle_get(connection, uri)
            elif method == 'POST':
                self.handle_post(connection, uri, body)
            elif method == 'PUT':
                self.handle_put(connection, uri, body)
            elif method == 'DELETE':
                self.handle_delete(connection, uri)
            else:
                response_data = self.build_error_response(400)
                connection.sendall(response_data)
                connection.close()

        except Exception as e:
            print(f"[error] {e}")
            self.send_response(connection, 500, "Internal Server Error")

    def handle_get(self, connection, uri):
        # Implement GET logic here
        # Example:
        self.send_response(connection, 200, "GET request received for " + uri)

    def handle_post(self, connection, uri, body):
        # Implement POST logic here
        # Example:
        self.send_response(connection, 200, "POST request received with body: " + body)

    def handle_put(self, connection, uri, body):
        # Implement PUT logic here
        # Example:
        self.send_response(connection, 200, "PUT request received for " + uri)

    def handle_delete(self, connection, uri):
        # Implement DELETE logic here
        # Example:
        self.send_response(connection, 200, "DELETE request received for " + uri)

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        conn_type = "HTTP"
        if self.is_https:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(self.cert_file, self.key_file)
            server_socket = context.wrap_socket(server_socket, server_side=True)
            conn_type = "HTTPS"
        print(f"[INFO] {conn_type} Server started on {self.host}:{self.port}\n")

        server_socket.listen(5)
        while True:
            connection, address = server_socket.accept()
            request = connection.recv(1024).decode('iso-8859-1')
            if request:
                self.handle_request(connection, request)
            connection.close()


if __name__ == "__main__":
    server = HTTPServer()
