import pos
import asyncio
import win32con
import websockets
import convertToDocx
from print import print_pdf, getPrinters
from dotenv import dotenv_values
import json

config = dotenv_values(".env")

async def handle_websocket(websocket, path):
    print("WebSocket connection established")
    try:
        while True:
            data = await websocket.recv()
            print(data)
            data = json.loads(data)
            
            if data['event'] == 'pos':
                res = pos.send(10000)
                print('**********result************')
                print(res)
                print('**********result************')
                await websocket.send(res)
                
            if data['event'] == 'print':
                print('****************print***************')
                print(data['context'])
                convertToDocx.run(data['template'],data['context'])
                pdf_file_path = ".\\print.docx"
                printer_name = config.get("PRINTER")
                paper_size = win32con.DMPAPER_A4  # Example: Set the paper size to A4
                print_pdf(pdf_file_path, printer_name, paper_size)
                
            if data['event'] == 'printers':
                res = getPrinters()
                await websocket.send(res)

    except websockets.ConnectionClosed:
        print("WebSocket connection closed")


start_server = websockets.serve(handle_websocket, "127.0.0.1", 8765)  # Replace with your desired IP and port
print("WebSocket server listening on ws://127.0.0.1:8765...")  # Replace with your IP and port
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
