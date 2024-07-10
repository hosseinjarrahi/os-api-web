import db
import json
import socket
import userpaths
from dotenv import dotenv_values
import json

my_docs = userpaths.get_my_documents()

config = dotenv_values(my_docs+"\\.env")

HOST = config.get("HOST")
PORT = config.get("PORT")

# Create a TCP socket

async def send(amount = 12000, url = ''):
    data = json.dumps({
        "cmd":10,
        "resp":0,
        "pan":"603799**7145",
        "rrn":"806524281275",
        "terminal":"99028391",
        "trace":"254395",
        "serial":"002167",
        "amount":"3218600",
        "settlement":"3218600",
        "discount":"0",
        "data1":"BK003\u00e3\u00e1\u00edDT012240706083437RL0011FP0012SP0011T9009236475393"
    })

    db.create(data,url)

    return data

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
        
        decodedRes = response.decode("latin-1")
        
        print(f'Received response from server: {decodedRes}')
        
        db.create(decodedRes,url)
        
        return decodedRes

    except Exception as e:
        print(f'Error: {e}')

    finally:
        # Close the connection
        connection.close()
        print('Connection closed')
