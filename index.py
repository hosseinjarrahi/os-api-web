import os
import pos
import json
import socket
import asyncio
import win32con
import threading
import userpaths
import websockets
import convertToDocx
from print import getPrinters
from dotenv import dotenv_values
from print import print_word_file, getPrinters

my_docs = userpaths.get_my_documents()

config = dotenv_values(my_docs+"\\.env")

print(
    'local ip => ' + socket.gethostbyname(socket.gethostname())
)

print(
    'local pos => ' + config.get("HOST")
)

print('**********SELECTED PRINTER***********')
print(config.get("PRINTER"))
print('**********SELECTED PRINTER***********')

print('**********all printers***********')
print(getPrinters())
print('**********all printers***********')

def custom_encoder(obj):
    if isinstance(obj, tuple):
        return {'__tuple__': True, 'items': list(obj)}
    return obj

async def runPos(websocket, data):
    print('***********pos***************')
    # for bypass pos
    # return await websocket.send('0020{"cmd":10,"resp":99}')
    # print(data)
    return await websocket.send('0020{"key":"' + data.get('key') + '","cmd":10,"resp":0,"pan":"603770**1285","rrn":"806720040564","terminal":"99028391","trace":"13880","serial":"003193","amount":"11135850","settlement":"11135850","discount":"0","data1":"BK007\u0098\u00d4\u00c7\u00e6\u00d1\u00d2\u00edDT012240727103513RL0011FP0012SP0011T9009236475393IB026IR400590047200404655354002"}')

    # print('send')
    # print(data['amount'])

    # res = await pos.send(data['amount'],data['url'])
    res = await pos.send(data.get('amount'), data.get('url'))
    
    # todo: should find { and then automaticly detect index of { and then insert key in string
    if 'key' in data:
        res = res[0:5] + '"key":"' + data.get('key') + '",' + res[5:]
    
    await websocket.send(res)

def printFile(data):
    print('****************print***************')
    count = data.get('count', 1)
    root_path = my_docs
    pdf_file_path = root_path + "\\print.docx"
    template_file_path = root_path + "\\" + data['template']
    convertToDocx.run(template_file_path, data['context'])
    printer_name = data.get("printer") if data.get("printer") else config.get("PRINTER")
    paper_size = win32con.DMPAPER_A4  # Example: Set the paper size to A4
    print_word_file(pdf_file_path, printer_name, paper_size,count)

async def handle_websocket(websocket):
    print("WebSocket connection established")
    try:
        while True:
            data = await websocket.recv()
            print(websocket, data)
            data = json.loads(data)
            
            if data['event'] == 'pos':
                await runPos(websocket,data)
            
            if data['event'] == 'print':
                threading.Thread(target=printFile, args=(data,)).start()
            
            if data['event'] == 'printers':
                res = getPrinters()
                
                json_data = json.dumps(res, default=custom_encoder)

                await websocket.send(json_data)

    except websockets.ConnectionClosed:
        print("WebSocket connection closed")


start_server = websockets.serve(handle_websocket, "0.0.0.0", 8765)  # Replace with your desired IP and port
print("WebSocket server listening on ws://0.0.0.0:8765...")  # Replace with your IP and port
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


