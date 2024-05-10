import socket
# Host and port configuration
HOST = ''
PORT = 50140 # Arbitrary non-reserved port
BUFFER_SIZE = 1024  # Size of the data to receive from the server

def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(BUFFER_SIZE).decode("utf-8").split(" ")
        request, number = message[0], message[1]  # Extract request type and number from the message
        response = process(request, number)  # Process the request and generate a response
        connectionSocket.send(response.encode("utf-8"))  # Send the response back to the client
    except socket.error as e:
        # Handle any socket errors that occur
        print(f"Socket error: {e}")
    finally:
        # Ensure the connection is closed after processing
        connectionSocket.close()
        
def validate_message(request, number):
    validation = 0b00  # Initialize validation as a 2-bit binary number which covers all 4 possible cases 
    if request in {"B", "H"}:
        validation |= 0b10 # Set the second bit to 1 if the request is valid
    if number.lstrip('-').isnumeric():  # Check if the number is numeric (allowing for a leading '-')
        validation |= 0b01 # Set the first bit to 1 if the number is valid
    return validation

def process(request, number): # Process the client's request. Validates the request and number, and returns a response based on the validation result.
    validation = validate_message(request, number)
    match validation: 
        case 0b00: 
            return "500" + " " + "Request is empty"
        case 0b01:
            return "300" + " " + "Bad request"
        case 0b10:
            return "400" + " " + "The number is missing"
        case 0b11:
            number = int(number)
            match request:
                case "B":
                    return "200" + " " + format(number, "b")  # Convert number to binary
                case "H":
                    return "200" + " " + format(number, "x")  # Convert number to hexadecimal

def start_server(HOST, PORT):
    # Start the server and listen for client connections and handle them
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
        socket.bind((HOST, PORT))  # Bind the socket to the specified host and port
        while True:
            socket.listen(5)  # Listen for connections, with a maximum number of 5 connections
            print("Listening...")
            
            connectionSocket = socket.accept()  # Accept a new connection
            print("Accepted connection")
            
            handle_client(connectionSocket)  # Handle the connected client

start_server(HOST, PORT)  # Call the function to start the server
