import socket
# Host and port configuration
HOST: str = "" # A blank string means that we listen to all incoming connections not just localhost, the client can use the server"s IP address to connect to it
PORT: int = 50140 # Arbitrary non-reserved port
BUFFER_SIZE: int = 1024  # Size of the data to receive from the server
DELIMITER: str = " " # A space is used to separate request type and number

        
def validate_message(request: str, number: str) -> int:
    """
    Validates the client's request and number, returning a 2-bit binary number that encodes the validation result.
    
    The validation result is encoded as follows:
    - Bit 0 (least significant bit): 1 if the number is valid, 0 if the number is invalid
    - Bit 1: 1 if the request is valid, 0 if the request is invalid
    
    Args:
        request (str): The request from the client, which can be "B" to convert the number to binary or "H" to convert the number to hexadecimal.
        number (str): The number to be converted.
    
    Returns:
        int: A 2-bit binary number that encodes the validation result.
    """
    validation = 0b00  # Initialize validation as a 2-bit binary number which covers all 4 possible cases 
    if request in {"B", "H"}:
        validation |= 0b10 # Set the second bit to 1 if the request is valid
    if number.lstrip("-").isdigit():  # Check if the number is valid (allowing for a leading "-" for negative numbers)
        validation |= 0b01 # Set the first bit to 1 if the number is valid
    return validation

def process(request: str, number: str) -> str:
    """
    Processes the client's request by validating the request and number, and returning a response based on the validation result.
    
    Args:
        request (str): The request from the client, which can be "B" to convert the number to binary or "H" to convert the number to hexadecimal.
        number (str): The number to be converted.
    
    Returns:
        str: A response string in the format "STATUS_CODE" + DELIMITER + "RESPONSE_MESSAGE", where:
            - STATUS_CODE is a 3-digit status code indicating the result of the request processing:
                - "200" for successful processing
                - "300" for a bad request
                - "400" for a missing number
                - "500" for an empty request
            - RESPONSE_MESSAGE is a string describing the result of the request processing.
    """
    validation = validate_message(request, number)
    match validation: 
        case 0b00: 
            return "500" + DELIMITER + "Request is empty"
        case 0b01:
            return "300" + DELIMITER + "Bad request"
        case 0b10:
            return "400" + DELIMITER + "The number is missing"
        case 0b11:
            number = int(number)
            match request:
                case "B":
                    return "200" + DELIMITER + format(number, "08b")  # Convert number to binary
                case "H":
                    return "200" + DELIMITER + format(number, "X")  # Convert number to hexadecimal

def handle_client(connectionSocket: socket.socket) -> None:
    """
    Handles a client connection by processing the client's request and sending a response back.
    
    Args:
        connectionSocket (socket.socket): The socket connection to the client.
    
    Raises:
        None
    
    Returns:
        None
    """
    try:
        message = connectionSocket.recv(BUFFER_SIZE).decode("utf-8").split(DELIMITER, 1)
        if len(message) != 2:
            return
        request, number = message[0], message[1]  # Extract request type and number from the message
        response = process(request, number)  # Process the request and generate a response
        connectionSocket.send(response.encode("utf-8"))  # Send the response back to the client
    finally:
        # Ensure the connection is closed after processing
        connectionSocket.close()

def start_server(HOST: str, PORT: int) -> None:
    """
    Starts a TCP server that listens for client connections and handles them.
    
    The server binds to the specified host and port, and listens for incoming connections.
    When a new connection is accepted, the `handle_client` function is called to handle the
    connected client.
    
    Args:
        HOST (str): The host address to bind the server socket to.
        PORT (int): The port number to bind the server socket to.
    """
    # Start the server and listen for client connections and handle them
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))  # Bind the socket to the specified host and port
        while True:
            server_socket.listen(5)  # Listen for connections, with a maximum number of 5 connections
            connectionSocket, addr = server_socket.accept()  # Accept a new connection
            handle_client(connectionSocket)  # Handle the connected client

start_server(HOST, PORT)  # Call the function to start the server
