import cv2
import time
import glob
import os
from mailing import send_mail
from threading import Thread

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(1)
first_frame = None
status_list = []
count = 1


while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    g_blur = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    if first_frame is None:
        first_frame = g_blur
    delta_frame = cv2.absdiff(first_frame, g_blur)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            capture_image = cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
    status_list.append(status)
    s = status_list[-2:]
    image = glob.glob(f"images/*.png")
    inde = int(len(image) / 2)
    #mjknjkn
    print("Length of 'image' list:", len(image))
    print("Value of 'inde':", inde)
    print("Value of 's[0]':", s[0])
    print("Value of 's[1]':", s[1])
    mail_thread = Thread(target=send_mail, args=(image[inde], ))
    send_mail.daemon = True
    if s[0] == 0 and s[1] == 1:
        mail_thread.start()
    #hbhbhj
    cv2.imshow("PJ", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

for i in image:
    if i != image[inde]:
        os.remove(i)
video.release()
