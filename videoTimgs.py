import cv2
import math
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def saveI(filename, frame):
    cv2.imwrite(filename, frame)


videoname = "fme.mp4"
imagesFolder = "data/{}img".format(videoname.split(".")[0])
if os.path.exists(imagesFolder):
    print(imagesFolder, "exist")
    exit()
else:
    os.mkdir(imagesFolder)
    print("mk", imagesFolder)

cap = cv2.VideoCapture("data/" + videoname)
frameRate = cap.get(5)  # frame rate
saveRate = int(frameRate * 0.5)
print("framerate: {} \n saverate: {}".format(frameRate, saveRate))
i = 0

begin = time.time()
# while cap.isOpened():
#     i += 1
#     frameId = cap.get(1)
#     ret, frame = cap.read()
#     if ret != True:
#         break
#     if frameId % saveRate == 0:
#         filename = imagesFolder + "/image_" + str(int(frameId)) + ".jpg"
#         cv2.imwrite(filename, frame)

with ThreadPoolExecutor(max_workers=20) as t:
    obj_list = []
    while cap.isOpened():
        i += 1
        frameId = cap.get(1)
        ret, frame = cap.read()
        if ret != True:
            break
        if frameId % saveRate == 0:
            filename = imagesFolder + "/image_" + str(int(frameId)) + ".jpg"
            t.submit(cv2.imwrite, filename, frame)

cap.release()
times = time.time() - begin
print("{}\nDone!".format(round(times, 2)))
