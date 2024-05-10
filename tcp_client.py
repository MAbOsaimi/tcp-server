import socket, sys

HOST = 'localhost'  # Server's IP
PORT = 50140  # Server's port
BUFFER_SIZE = 1024  # Size of the data to receive from the server

def send_request(request, number):
    # Combine the request type and number and separate them by a space
    message = request + " " + str(number)

    # Define the socket and its config (It uses IPv4 and TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
        socket.settimeout(60)  # Set timeout to 60 seconds
        try:
            # Initiate connection request to socket with the given host and port numbers
            socket.connect((HOST, PORT))
            # Encode the message with utf-8
            socket.send(message.encode("utf-8"))
            # Receive the expected 1024 bytes and decode them
            response = socket.recv(BUFFER_SIZE).decode("utf-8")
            print(response)
        except ConnectionRefusedError:
            print("Server is down, please try later.")
        except socket.error as e:
            print(f"Socket error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def main():
    request = input("""B: to convert to binary
H: to convert to hexadecimal
Q: to quit the client program
Enter request: """)

    if request == "Q":
        sys.exit(0)

    # Number to be added to the message payload
    number = input("Enter number to be converted: ")

    send_request(request, number)

if __name__ == "__main__":
    main()
