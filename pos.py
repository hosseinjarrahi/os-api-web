import socket
import json
from dotenv import dotenv_values

config = dotenv_values(".env")

HOST = config.get("HOST")
PORT = config.get("PORT")

# Create a TCP socket

def send(amount = 12000):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the specified address and port
        connection.connect((HOST, int(PORT)))
        print('Connected to server')

        # Prepare data
        data = {
            'cmd': 10,
            'amount': amount,
            'sign': '899|123456789',
            'swipe': True,
        }
        data_str = json.dumps(data)
        data_str = '00' + str(len(data_str)) + data_str
        bytes_data = bytes(data_str, 'utf-8')

        # Send the data to the server
        connection.sendall(bytes_data)
        print('Data sent successfully')

        # Receive the response from the server
        response = connection.recv(1024)  # Adjust buffer size as per your requirements
        decodedRes=response.decode("latin-1")
        print(f'Received response from server: {decodedRes}')
        return decodedRes

    except Exception as e:
        print(f'Error: {e}')

    finally:
        # Close the connection
        connection.close()
        print('Connection closed')
