from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import darknet
import datetime
import mss
import aimbot
from PIL import Image
sct = mss.mss()
monitor = {'left': 752, 'top': 332, 'width': 416, 'height': 416}
path = os.path.join('data/csmodels/fbi')
imglist = []

name2bh = ['fbih', 'fbi']

netMain = [None, None]
metaMain = [None, None]
altNames = [None, None]
now = datetime.datetime.now()
# NewImageName = None


def convertBack(x, y, w, h):
  xmin = int(round(x - (w / 2)))
  xmax = int(round(x + (w / 2)))
  ymin = int(round(y - (h / 2)))
  ymax = int(round(y + (h / 2)))
  return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img, fps):
  for detection in detections:
    x, y, w, h = detection[2][0],\
        detection[2][1],\
        detection[2][2],\
        detection[2][3]
    xmin, ymin, xmax, ymax = convertBack(
        float(x), float(y), float(w), float(h))
    pt1 = (xmin, ymin)
    pt2 = (xmax, ymax)
    cl = (255, 236, 139)if detection[0].decode() == 't' else(65, 105, 225)
    cv2.rectangle(img, pt1, pt2, cl, 1)
    cv2.putText(img,
                detection[0].decode()
                + " [" + str(round(detection[1] * 100, 2)) + "]",
                (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                cl, 2)
  cv2.putText(img, str(fps), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
              [0, 255, 0], 2)
  return img


def getImglist():
  fl = os.listdir(path)
  global imglist
  for fn in fl:
    if fn.endswith('.jpg'):
      imglist.append(fn.split('.')[0])


def init(configPath="cfg/yolov4-custom.cfg", weightPath="backup_3/yolov4-custom_7000.weights", metaPath="cfg/voc.data", index=0):
  global metaMain, netMain, altNames  # pylint: disable=W0603

  if netMain[index] is None:
    netMain[index] = darknet.load_net_custom(
        configPath.encode("ascii"), weightPath.encode("ascii"), 0, 1
    )  # batch size = 1
  if metaMain[index] is None:
    metaMain[index] = darknet.load_meta(metaPath.encode("ascii"))
  if altNames[index] is None:
    # In Python 3, the metafile default access craps out on Windows (but not Linux)
    # Read the names file and create a list to feed to detect
    try:
      with open(metaPath) as metaFH:
        metaContents = metaFH.read()
        import re

        match = re.search(
            "names *= *(.*)$", metaContents, re.IGNORECASE | re.MULTILINE
        )
        if match:
          result = match.group(1)
        else:
          result = None
        try:
          if os.path.exists(result):
            with open(result) as namesFH:
              namesList = namesFH.read().strip().split("\n")
              altNames[index] = [x.strip() for x in namesList]
        except TypeError:
          pass
    except Exception:
      pass


def savebody_head(detections, NewImageName, yolobh):
  saveimg = False

  for detection in detections:
    if float(detection[1]) < 0.25:
      continue
    cx, cy, w, h = float(detection[2][0]),\
        float(detection[2][1]),\
        float(detection[2][2]),\
        float(detection[2][3])
    with open(path + '/' + NewImageName + '.txt', 'a+' if yolobh == 1 else 'w') as f:
      f.write("{} {} {} {} {}\n".format(yolobh, round(
          cx / 416, 16), round(cy / 416, 16), round(w / 416, 16), round(h / 416, 16)))
    if saveimg == True:
      continue
    saveimg = True
    xmin, ymin, xmax, ymax = convertBack(
        float(cx), float(cy), float(w), float(h))

    padw = int(float(w) * 0.15)
    padh = int(float(h) * 0.1)
    if aimbot.BoolShot(600) == False:
      continue
    aimbot.moveMouse(int((xmin + xmax) / 2), int((ymin + ymax) / 2))
    # if xmin + padw < 208 and xmax - padw > 208 and ymin + padh < 208 and ymax - padh > 208:
    aimbot.shot()

    print(yolobh, NewImageName, detection)

  return saveimg


def YOLO():

  global metaMain, netMain, altNames, imglist

  # Create an image we reuse for each detect
  # darknet_image = [darknet.make_image(darknet.network_width(netMain[0]),
  #                                     darknet.network_height(netMain[0]), 3), darknet.make_image(darknet.network_width(netMain[1]),
  #                                                                                                darknet.network_height(netMain[1]), 3)]
  darknet_image = darknet.make_image(darknet.network_width(netMain[0]),
                                     darknet.network_height(netMain[0]), 3)
  last_save = time.time()

  i = len(imglist)

  while True:
    prev_time = time.time()

    while "{}_{}_{}_{}".format(now.year, now.month, now.day, i) in imglist:
      i += 1
    NewImageName = "{}_{}_{}_{}".format(now.year, now.month, now.day, i)

    st = sct.grab(monitor)
    frame_resized = cv2.cvtColor(np.array(st), cv2.COLOR_BGR2RGB)
    darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())

    detections = darknet.detect_image(
        netMain[0], metaMain[0], darknet_image, thresh=0.25)
    if savebody_head(detections, NewImageName, 0) == True and time.time() - last_save > 1:
      last_save = time.time()
      imglist.append(NewImageName)
      Image.frombytes("RGB", st.size, st.bgra, "raw", "BGRX").save(
          path + '/{}.jpg'.format(NewImageName), quality=100, subsampling=0)

    image = cvDrawBoxes(detections, frame_resized,
                        1 / (time.time() - prev_time))

    # detections = darknet.detect_image(
    #     netMain[1], metaMain[1], darknet_image[1], thresh=0.5)
    # res = savebody_head(detections, NewImageName, 1)

    # if res and not (NewImageName in imglist) and time.time() - last_save > 1:
    #   last_save = time.time()
    #   print("body add ", NewImageName)
    #   imglist.append(NewImageName)
    #   Image.frombytes("RGB", st.size, st.bgra, "raw", "BGRX").save(
    #       path + '/{}.jpg'.format(NewImageName), quality=100, subsampling=0)
    # image = cvDrawBoxes(detections, image)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imshow('Demo', image)
    cv2.waitKey(3)


if __name__ == "__main__":
  getImglist()
  init()
  # init(configPath='cfg/yolov3-voc.cfg',
  #      weightPath='backup/yolov3-voc_last.weights', metaPath='cfg/voc3.data', index=1)
  YOLO()
