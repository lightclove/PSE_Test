from socket import socket

from eclient import raw_input

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = raw_input("Server Address To Be Connected -> ")
port = int(input("Port of The Server -> "))
server.connect((host, port))