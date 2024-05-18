import os
import pos
import json
import asyncio
import win32con
import threading
import userpaths
import websockets
import convertToDocx
from print import getPrinters
from dotenv import dotenv_values
from print import print_pdf, getPrinters

my_docs = userpaths.get_my_documents()

config = dotenv_values(my_docs+"\\.env")

print(my_docs+"\\.env")

print('**********SELECTED PRINTER***********')
print(config.get("PRINTER"))
print('**********SELECTED PRINTER***********')

print('**********all printers***********')
print(getPrinters())
print('**********all printers***********')

async def runPos(websocket,data):
    print('***********pos***************')
    # for bypass pos
    # return await websocket.send('ok')
    print('send')
    print(data['amount'])

    res = await pos.send(data['amount'])
    await websocket.send(res)

def printFile(data):
    print('****************print***************')
    print(data['context'])
    count = data.get('count',1)
    root_path = my_docs
    pdf_file_path = root_path + "\\print.docx"
    template_file_path = root_path + "\\" + data['template']
    convertToDocx.run(template_file_path,data['context'])
    printer_name = config.get("PRINTER")
    print(printer_name)
    paper_size = win32con.DMPAPER_A4  # Example: Set the paper size to A4
    for i in range(1, count + 1):
        print_pdf(pdf_file_path, printer_name, paper_size)

async def handle_websocket(websocket):
    print("WebSocket connection established")
    try:
        while True:
            data = await websocket.recv()
            print(websocket,data)
            data = json.loads(data)
            
            if data['event'] == 'pos':
                await runPos(websocket, data)
                
            if data['event'] == 'print':
                printFile(data)
                
            if data['event'] == 'printers':
                res = getPrinters()
                print('*****************************')
                print(type(res))
                print('*****************************')
                await websocket.send(res)

    except websockets.ConnectionClosed:
        print("WebSocket connection closed")


start_server = websockets.serve(handle_websocket, "127.0.0.1", 8765)  # Replace with your desired IP and port
print("WebSocket server listening on ws://127.0.0.1:8765...")  # Replace with your IP and port
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
