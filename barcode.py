import cv2
import numpy as np
from pyzbar.pyzbar import decode
import dco
import os

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
print('hello')

processed_data = set()

dco.decoded_numbers
with open('debarcodedata.txt') as f:
    mydatalist = f.read().splitlines()
print(mydatalist)

while True:
    success, img = cap.read()
    for barcode in decode(img):
        mydata = barcode.data.decode('utf-8').strip()
        if mydata not in processed_data:
            print(mydata)
            processed_data.add(mydata)
            if mydata in mydatalist:
                print('authorized')
            else:
                print('un-authorized')

    cv2.imshow('result', img)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()

# Delete the debarcodedata.txt file
os.remove('debarcodedata.txt')
