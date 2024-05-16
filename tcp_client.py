import socket, sys, random

HOST = "localhsot"  # Server's IP
PORT: int = 50140  # Server's port
BUFFER_SIZE: int = 1024  # Size of the data to receive from the server
ERROR_RATE: float = 0.2 # Arbitrary error rate to simulate corruption of data (there is less than ERROR_RATE possibility of corrupting data)


def randomly_corrupt(data: str) -> str:
    """Randomly corrupt the input data with a given error rate.
    
    If the error rate is met, return a random uppercase letter. Otherwise, return the original data.
    
    Args:
        data (str): The input data to potentially corrupt.
    
    Returns:
        str: The corrupted or original data.
    """
    if random.random() < ERROR_RATE:
            return random.choice('ACDEFGIJKLMNOPQRSTUVWXYZ')  # Return a random invalid input
    return data  # If not corrupting, return the original data

def display_response(status_code: int, message: str) -> None:
        """
        Displays the response from the server.
        
        Args:
            status_code (int): The HTTP status code returned by the server.
            message (str): The message returned by the server.
        
        Raises:
            ValueError: If the status code is not 200 (OK).
        """
        if status_code == 200:
            print(message)
        else:
            print(message)
            raise ValueError(message)

def send_request(request: str, number: str, client_socket: socket.socket) -> None:
    """
    Sends a request to the server with the given request type and number, and displays the server's response.
    
    Args:
        request (str): The type of request to send, either "B" for binary conversion or "H" for hexadecimal conversion.
        number (str): The number to be converted.
        client_socket (socket.socket): The socket object to use for communication with the server.
    
    Raises:
        socket.error: If a socket error occurs during the request.
    """
    
    # Combine the request type and number and separate them by a space
    message = randomly_corrupt(request) + " " + randomly_corrupt(str(number))

    try:
        # Encode the message with utf-8
        client_socket.send(message.encode("utf-8"))
        # Receive the expected 1024 bytes and decode them
        status_code, message = client_socket.recv(BUFFER_SIZE).decode("utf-8").split(" ", 1)
        status_code = int(status_code)
        display_response(status_code, message)
    except socket.error as e:
        print(f"Socket error: {e}")
    
            
def main() -> None:
    # Define the socket and its config (It uses IPv4 and TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.settimeout(60)  # Timeout after 60 seconds of inactivity
        try:
            # Initiate connection request to socket with the given host and port numbers
            client_socket.connect((HOST, PORT))
            while True:
                request = input("""B: to convert to binary
H: to convert to hexadecimal
Q: to quit the client program
Enter request: """).upper()

                if request not in ["B", "H", "Q"]:
                    print("Invalid choice. Please enter B, H, or Q.")
                    continue

                if request == "Q":
                    sys.exit(0)

                while True:
                    number = input("Enter number to be converted: ")
                    if number.isdigit():
                        break
                    else:
                        print("Invalid input. Please enter a number.")
                break
            send_request(request, number, client_socket)
        except ConnectionRefusedError:
            print("Server is down, please try later.")
        finally:
            client_socket.close()

if __name__ == "__main__":
    main()
