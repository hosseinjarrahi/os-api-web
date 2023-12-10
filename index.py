import asyncio
import websockets
import send

async def handle_websocket(websocket, path):
    print("WebSocket connection established")
    try:
        while True:
            # Receive data from the WebSocket
            data = await websocket.recv()
            # Process the data or forward it to the POS system via raw TCP
            print(f"Received data: {data}")
            if data['event'] == 'pos':
                res = send.send()
                await websocket.send(res)
            # Forward the data to the POS system using raw TCP (implement this part)
            # ...
    except websockets.ConnectionClosed:
        print("WebSocket connection closed")

# Start the WebSocket server
start_server = websockets.serve(handle_websocket, "127.0.0.1", 8765)  # Replace with your desired IP and port
print("WebSocket server listening on ws://127.0.0.1:8765...")  # Replace with your IP and port
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
