import socket
import ssl
import threading


def handler(conn):
	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
	context.verify_mode = ssl.CERT_NONE
	context.load_cert_chain(certfile="./demo.crt", keyfile="./demo.key", password=None)
	s_conn = context.wrap_socket(conn, server_side=True)
	#print(1)
	resp = "HTTP/1.1 200 OK/r/n"
	resp += "Content-Type: text/html\r\n"
	body = "<b>Hello!</b>"
	resp += "Content-Length: " + str(len(body)) + "\r\n\r\n"
	resp += body
	resp += "\r\n"
	#print(1)
	s_conn.send(resp.encode())
	#print(1)
	s_conn.close()


if __name__ == "__main__":
	#print(1)
	srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#print(1)
	srv.bind(("localhost", 443))
	srv.listen(5)

	while True:
		#print(1)
		connection, addr = srv.accept()
		#print(1)
		t = threading.Thread(target=handler, args=(connection,))
		t.start()
