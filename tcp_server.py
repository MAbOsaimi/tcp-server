import socket

def validate_message(request, number):
    validation = ["0", "0"]
    if request == "B" or request == "H":
        validation[0] = "1"
    if number.isnumeric():
        validation[1] = "1"
    return validation

def process(request, number):
    validation = "".join(validate_message(request, number))
    match validation:
        case "00":
            return "500" + "|" + "Request is empty"
        case "01":
            return "300" + "|" + "Bad request"
        case "10":
            return "400" + "|" + "The number is missing"
        case "11":
            number = int(number)
            match request:
                case "B":
                    return "200" + "|" + bin(number)[2:]
                case "H":
                    return "200" + "|" + hex(number)[2:]

HOST = 'localhost'
PORT = 64221 # Arbitrary non-reserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

while True:
    server.listen(0)
    connectionSocket, addr = server.accept()
    try:
        request, number = connectionSocket.recv(1024).decode("utf-8").split("|")
        print(request)
        print(number)
        response = process(request, number)
        connectionSocket.send(response.encode("utf-8"))
    finally:
        connectionSocket.close()