#Program for face recognition + data extraction

import cv2
import pytesseract
import numpy as np
import face_recognition
import os
from datetime import datetime
from tabulate import tabulate
from pathlib import Path

#Source
mydata = [{"1", "AADHAR"}, {"2", "PAN"}]
head = ["Type", "Source"]
print(tabulate(mydata, headers=head, tablefmt="grid"))
source = int(input('Enter your type = '))
print('\nloading...')
for n in range (4):
    if (source!=1 and source!=2):
        print('\nInput type does not exist, retry\n')
        source = int(input('Enter your type = '))
    else:
        break
if (source != 1 and source != 2):
    print('\nMaximum number of tries exceeded!\nTry again later')
    exit()

#Input
mydata = [{"1", "Images"}, {"2", "Video"}, {"3", "Webcam"}]
head = ["Type", "Nature of input data"]
print(tabulate(mydata, headers=head, tablefmt="grid"))
Choice = int(input('Enter your type = '))
if (Choice == 1 or Choice == 2):
    file_name = input ('Enter file name (Without extension): ')
print('\nloading...')
for n in range (4):
    if (Choice!=1 and Choice!=2 and Choice!=3):
        print('\nInput type does not exist, retry\n')
        Choice = int(input('Enter your type = '))
    else:
        break
if (Choice != 1 and Choice != 2 and Choice != 3):
    print('\nMaximum number of tries exceeded!\nTry again later')
    exit()

#Working on input folder
path = 'Source'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:

    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

#Finding encodings from source
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

#Marking on excel file
def marking(name):
    with open('Result.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            if (source == 1):
                f.writelines(f'\n{name},{dtString},{N},{Name},{Ad}')
            else:
                f.writelines(f'\n{name},{dtString},{N},{Name}')
encodeListKnown = findEncodings(images)
print('\nEncoding Complete\n')

def remove_last_line_from_string(s):
    return s[:s.rfind('\n')]

#Extracting details from source
def extraction():
    pytesseract.pytesseract.tesseract_cmd = r"C:\... \tesseract.exe" #Enter your location
    image = cv2.imread(r"C:\Users\... \Verification\Source\\" + name + '.jpg', 0)
    thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    print('Match Found:')
    if (source==1):
        #AADHAR Number
        x,y,w,h = 465, 2200, 420, 57
        ROI = thresh[y:y+h,x:x+w]
        N = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6')
        print('AADHAR : '+ N)
        N = remove_last_line_from_string(N)
        #AADHAR Name
        x,y,w,h = 310, 1270, 700, 40
        ROI = thresh[y:y+h,x:x+w]
        Name = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6')
        print('Name : '+ Name)
        Name = remove_last_line_from_string(Name)
        # AADHAR Address
        x, y, w, h = 1270, 2708, 650, 250
        ROI = thresh[y:y + h, x:x + w]
        Ad = pytesseract.image_to_string(ROI, lang='eng', config='--psm 6')
        Ad = remove_last_line_from_string(Ad)
        print('Address :\n' + Ad)
    else:
        #Pan Number
        x,y,w,h = 1050, 720, 341, 64
        ROI = thresh[y:y+h,x:x+w]
        N = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6')
        N = remove_last_line_from_string(N)
        print('Pan : '+ N)
        #PAN Name
        x,y,w,h = 930, 860, 800, 60
        ROI = thresh[y:y+h,x:x+w]
        Name = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6')
        Name = remove_last_line_from_string(Name)
        print('Name : '+ Name)
    marking(name)
    exit()

#Match checking
if (Choice == 1):
    address = (r"C:\Users\... Verification\Input\\") #Enter your location
    path = Path(address + file_name + '.jpg')
    path2 = Path(address + file_name + '.png')
    if path.is_file():
        img = cv2.imread(address + file_name + '.jpg', 0)
    elif path2.is_file():
        img = cv2.imread(address + file_name + '.png', 0)
    else:
        print('Incorrect file name')
        exit()
    while True:
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                extraction()
            else:
                print('No match found')
                exit()
elif (Choice == 2):
    path = Path(address + file_name + '.mkv')
    path2 = Path(address + file_name + '.avi')
    path3 = Path(address + file_name + '.mp4')
    if path.is_file():
        cap = cv2.VideoCapturer(address + file_name + '.mkv')
    elif path2.is_file():
        cap = cv2.VideoCapture(address + file_name + '.avi')
    elif path3.is_file():
        cap = cv2.VideoCapture(address + file_name + '.mp4')
    else:
        print('Incorrect file name')
        exit()
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                extraction()
            else:
                print('No match found')
                exit()
else:
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
#                Display Face
#                y1, x2, y2, x1 = faceLoc
#                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                extraction()
            else:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, 'NO MATCH', (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 2)
        cv2.imshow('Press ''Q'' to quit', img)
        key = cv2.waitKey(1)
        if key == 81 or key == 113:
            break
    cap.release()
    cv2.destroyAllWindows()