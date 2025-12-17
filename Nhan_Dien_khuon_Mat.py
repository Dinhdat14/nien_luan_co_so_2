import cv2
import os
import face_recognition
import numpy as np
import datetime

path = 'dataSet_1' 
images = []  
className = []
myList = os.listdir(path)  # Kiem tra toan bo ten file trong path

for i in myList:
    curimg = cv2.imread(f"{path}/{i}")  # Doc duong dan cua buc anh hien tai --> dataSet/34.jpg
    images.append(curimg)
    className.append(os.path.splitext(i)[0]) #tach filename va phan mo rong
# print(className)
# print(len(images))

# Mã hóa hình ảnh khuôn mặt
def Mahoa(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]  # mã hóa hình ảnh khuôn mặt
        encodeList.append(encode)
    return encodeList

encodeListKnow = Mahoa(images)  # hình ảnh có trong list ds thì in ra mã hóa
print("MÃ HÓA THÀNH CÔNG")


def thamdu(name):
    with open("thamdu.csv", 'r+') as f:         # mở file thamdu.csv ở trạng thái đọc và ghi
        myDatalist = f.readlines()
        nameList = []
        for line in myDatalist:
            entry = line.split(",")  # tach theo dau ,
            nameList.append(entry[0])

        if name not in nameList:
            now = datetime.datetime.now()  # tra ve ngay gio 2025-11-06 20:29:58.681296
            dtstring = now.strftime("%H:%M:%S")
            f.writelines(f"\n{name},{dtstring}")


# Khởi động Webcam
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    framE = cv2.resize(frame, (0, 0), None, fx=0.5, fy=0.5)  # tỉ lệ hình ảnh hiển thị bằng 50% hình ảnh gốc
    framE = cv2.cvtColor(framE, cv2.COLOR_BGR2RGB)
    # Xác định vị trí khuôn mặt
    facecurFrame = face_recognition.face_locations(framE)  # lay tung vi tri tren khuon mat hien tai
    encodecurFrame = face_recognition.face_encodings(framE)
    
    for encodeFace, faceLocations in zip(encodecurFrame, facecurFrame):  # lay tung vi tri tren khuon mat hien tai theo cap
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
        print(faceDis)  # in khoảng cách khuôn mặt hiện tại với khuôn mặt trong ds
        matchIndex = np.argmin(faceDis)
        if matches:
            if faceDis[matchIndex] < 0.50: # ngưỡng khoảng cách khuôn mặt
                name = className[matchIndex].upper()
                thamdu(name)
            else:
                name = 'Unknow_close'
        else:
            name = 'Unknow'

        # vẽ tên ra màn hình
        y1, x2, y2, x1 = faceLocations
        y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
        color = (0, 255, 0) if name not in ['Unknow', 'Unknow_close'] else (0, 0, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, name, (x2, y2), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, f"faceDis: {faceDis[matchIndex]:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow("Mô hình Nhận diện khuôn mặt", frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()  # giai phong camera
cv2.destroyAllWindows()  # thoat tat ca cac cua so