from qreader import QReader
import cv2

def decodeQR(path):
    qreader = QReader()

    image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)

    decoded_text = qreader.detect_and_decode(image=image)

    return decoded_text
