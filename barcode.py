import cv2
import numpy as np
from pyzbar.pyzbar import decode
import dco
import os

def scan():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    dco.decoded_numbers
    with open('debarcodedata.txt') as f:
        mydatalist = f.read().splitlines()


    while True:
        success, img = cap.read()
        for barcode in decode(img):
            mydata = barcode.data.decode('utf-8').strip()

            if mydata in mydatalist:
                myoutput = 'entered data'
            else:
                myoutput = 'invalid data'

            return mydata
        cv2.imshow('result', img)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

    # Delete the debarcodedata.txt file
    os.remove('debarcodedata.txt')

scan()