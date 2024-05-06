import socket

HOST = 'localhost' # Server's IP
PORT = 64221 # Server's port

request = input("""Enter request\nB: to convert to binary
H: to convert to hexadecimal
Q: to quit the client program\n""")

number = input("Enter number to be converted: ")

message = request + "|" + str(number)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    socket.connect((HOST, PORT))
    socket.send(message.encode("utf-8"))
    response = socket.recv(1024)
    print(response)
except ConnectionRefusedError:
    print("Server is down, please try later.")
finally:
    socket.send(message.encode("utf-8"))

