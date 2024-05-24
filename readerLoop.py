import os
import requests
import userpaths
import threading
from time import sleep
from pathlib import Path
from qrReader import decodeQR
from dotenv import dotenv_values

my_docs = userpaths.get_my_documents()

config = dotenv_values(my_docs+"\\.env")

baseURL = config.get('SERVER')

rootPath = os.path.dirname(os.path.realpath(__file__))

image_dir = my_docs + '\\scan'

def sendFile(file_path):
    url = baseURL + '/api/upload-file'

    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files)

    res = response.json()

    return res.get('link')

def updateInvoice(invoiceNumber,img):
    print(invoiceNumber)
    
    link = sendFile(img)

    data = {
        "invoice_number":invoiceNumber,
        "img":link
    }

    res = requests.post(baseURL + '/api/contract/update/data',data=data)

    print(res)

def loopOCR():
    while True:
        sleep(2)
        for filename in os.listdir(image_dir):

            if not filename.startswith('S-ADD'):
                
                try:
                    file_path = os.path.join(image_dir, filename)

                    code = decodeQR(file_path)
                    
                    code = code[0]

                    new_file_path = os.path.join(image_dir, code + '.jpg')
                    
                    os.rename(file_path, new_file_path)

                except Exception as e:
                    print(f"Error opening image {filename}: {e}")
                    
def loopUpload():
    while True:
        sleep(2)
        for filename in os.listdir(image_dir):

            filenameWithoutExtension = Path(filename).stem

            if filenameWithoutExtension.startswith('S-ADD') and not filenameWithoutExtension.endswith('_'):
                
                try:
                    file_path = os.path.join(image_dir, filename)

                    new_file_path = os.path.join(image_dir, filenameWithoutExtension + '_.jpg')
                    
                    updateInvoice(filenameWithoutExtension, file_path)
                    
                    os.rename(file_path, new_file_path)

                except Exception as e:
                    print(f"Error opening image {filename}: {e}")
       
print('start reading')  

loopOCR()
          
# threading.Thread(target=loopOCR).start()
# threading.Thread(target=loopUpload).start()
