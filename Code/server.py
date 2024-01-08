import os
import socket
import ssl
import subprocess
import sys
import datetime
import mimetypes
import tempfile
from http_parser import parse_request


class HTTPServerI:
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

    POST_ENV_VARS = {
        "QUERY_STRING": "",
        "SCRIPT_NAME": "",
        "SCRIPT_FILENAME": "",
        "REQUEST_METHOD": "POST",
        "GATEWAY_INTERFACE": "CGI/1.1",
        "REDIRECT_STATUS": '1',
        "CONTENT_TYPE": 'application/x-www-form-urlencoded',
        "CONTENT_LENGTH": '0',
        "REMOTE_HOST": ""
    }
    def logger(self, request):
        timestamp = datetime.datetime.now()
        server_log = f"[{timestamp}] {request}"
        print(server_log)
        with open('server.log', 'a') as log_file:
            log_file.write(server_log + "\n")

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

    def __init__(self):
        if not (3 <= len(sys.argv) <= 5):
            print("Usage: python server.py <host> <port> [<cert_file> <key_file>]")
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

    def send_error_response(self, status_code):
        status_text = self.STATUS.get(status_code, 'Unknown Error')
        content = f"<h1>{status_code} {status_text}</h1>".encode('iso-8859-1')
        content_type = 'text/html'
        response = f"HTTP/1.1 {status_code} {status_text}\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n"
        return response.encode('iso-8859-1') + content

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
        print(conn_type)

        while True:
            try:
                connection, address = server_socket.accept()
                request = connection.recv(1024).decode('iso-8859-1')

                if request:
                    self.handle_request(connection, address, request)
                else:
                    connection.close()
            except Exception as e:
                print(f"[error] {e}")

    def handle_request(self, connection, address, request):
        print(f"[INFO]  {'HTTPS' if self.is_https else 'HTTP'} connection from {address}\n")
        try:
            request_details = parse_request(request)
            if len(request_details) == 1:
                response_data = self.send_error_response(request_details[0])
                connection.sendall(response_data)
                connection.close()
                return
            method, uri, http_version, headers, body, query_params = request_details
            self.logger(f"{method} {uri} {http_version}")
            absolute_path = os.path.join(os.getcwd(), uri.lstrip('/'))

            if not os.path.isfile(absolute_path):
                response_data = self.send_error_response(404)
                connection.sendall(response_data)
                connection.close()
                return
            resp = None
            abs_path = os.path.join(os.getcwd(), absolute_path.lstrip('/'))
            if method == "GET":
                resp = self.get_response(absolute_path, query_params)
            elif method == "POST":
                resp = self.post_response(absolute_path, headers, body)
            elif method == "PUT":
                resp = self.put_response(absolute_path, headers, body)
            elif method == "DELETE":
                print("Hello")

            connection.sendall(resp)
            connection.close()

        except Exception as e:
            print(f"[error] {e}")
            self.send_response(connection, 500, "Internal Server Error")

    def build_success_response(self, content, content_type):
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n"
        return response.encode('iso-8859-1') + content

    def read_file_content(self, path):
        try:
            with open(path, 'rb') as f:
                content = f.read()
                content_type = mimetypes.guess_type(path)[0] or 'application/octet-stream'
                return content, content_type
        except IOError as e:
            print(f"[error] {str(e)}")
            return None, None

    def run_php_script(self, path):
        try:
            process = subprocess.Popen(['php', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            content, stderr_data = process.communicate()

            if process.returncode != 0:
                print(f"[error] {stderr_data.decode('iso-8859-1')}")
                return None, None

            return content, 'text/html'
        except Exception as e:
            print(f"[error] {str(e)}")
            return None, None

    def process_file(self, path):
        file_extension = os.path.splitext(path)[1]

        if file_extension == '.php':
            return self.run_php_script(path)
        else:
            return self.read_file_content(path)

    def build_error_response(self):
        content = "File not found or error in processing".encode('iso-8859-1')
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n\r\n".format(
            len(content))
        return response.encode('iso-8859-1') + content

    def get_response(self, path, query_params):
        content, content_type = self.process_file(path)

        if content is None:
            return self.build_error_response()

        query_params_str = "\n".join([f"{key}: {value}" for key, value in query_params.items()])
        modified_content = content + f"\n\nQuery Parameters:\n{query_params_str}".encode('iso-8859-1')

        return self.build_success_response(modified_content, content_type)

    def post_response(self, path, headers, body):
        content, content_type = self.process_post_request(path, headers, body)

        if content is None:
            return self.build_error_response()

        return self.build_success_response(content, content_type)

    def process_post_request(self, path, headers, body):
        file_extension = os.path.splitext(path)[1]

        if file_extension == '.php':
            return self.execute_php_script(path, headers, body)
        else:
            return self.read_file_content(path)

    def execute_php_script(self, path, headers, body):

        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            tmp.write(body)
            tmp_path = tmp.name

        env_vars = self.prepare_php_environment(path, headers, body)
        env_vars['PHP_POST_FILE'] = tmp_path

        try:
            process = subprocess.Popen(['php', path], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, env=env_vars)
            content, stderr_data = process.communicate()

            if stderr_data:
                print(f"[debug] PHP script stderr: {stderr_data.decode('iso-8859-1')}")

            return content, 'text/html'
        except Exception as e:
            print(f"[error] {str(e)}")
            return None, None


    def prepare_php_environment(self, path, headers, body):
        env_vars = self.POST_ENV_VARS.copy()
        # Add or modify environment variables as needed
        env_vars.update({
            'REQUEST_METHOD': 'POST',
            'CONTENT_LENGTH': headers['Content-Length'],
            'CONTENT_TYPE': headers.get('Content-Type', 'application/x-www-form-urlencoded'),
            'SCRIPT_FILENAME': path,
            'SCRIPT_NAME': os.path.basename(path),
            'POST_DATA': body
        })

        merged_env_vars = os.environ.copy()
        merged_env_vars.update(env_vars)
        return merged_env_vars

    def build_put_response(self, path, body):
        try:
            # Writing or overwriting the file at the specified path with the body of the PUT request
            with open(path, 'wb') as f:
                f.write(body.encode('iso-8859-1'))

            return self.build_success_response_put(path)
        except Exception as e:
            print(f"[error] Unable to process PUT request: {str(e)}")
            return self.build_error_response()

    def build_success_response_put(self, path):
        response = f"HTTP/1.1 201 Created\r\nContent-Location: {path}\r\n\r\n"
        return response.encode('iso-8859-1')

if __name__ == "__main__":
    server = HTTPServerI()
