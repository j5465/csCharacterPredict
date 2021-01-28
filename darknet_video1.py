import random
import os
import cv2
import numpy as np
import time
import darknet
import win32api
from math import sqrt
import mss
import aimbot
import threading
monitor = {}
netMain = None
metaMain = None
altNames = None
me = 't'
shotflag = False
Yolowidth = 288


def init(configPath="cfg/yolov4-custom.cfg", weightPath="backup_3/yolov4-custom_7000.weights", metaPath="cfg/voc.data"):
  global metaMain, netMain, altNames  # pylint: disable=W0603

  if netMain is None:
    netMain = darknet.load_net_custom(
        configPath.encode("ascii"), weightPath.encode("ascii"), 0, 1
    )  # batch size = 1
  if metaMain is None:
    metaMain = darknet.load_meta(metaPath.encode("ascii"))
  if altNames is None:
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
              altNames = [x.strip() for x in namesList]
        except TypeError:
          pass
    except Exception:
      pass


def convertBack(x, y, w, h):
  xmin = int(round(x - (w / 2)))
  xmax = int(round(x + (w / 2)))
  ymin = int(round(y - (h / 2)))
  ymax = int(round(y + (h / 2)))
  return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img, fps):
  for detection in detections:
    if float(detection[1]) < 0.5:
      continue
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
                detection[0].decode() +
                " [" + str(round(detection[1] * 100, 2)) + "]",
                (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                cl, 2)
  cv2.putText(img, str(fps), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
              [0, 255, 0], 2)
  return img


class Arec:
  x = None
  y = None
  tp = None

  def __init__(self, x, y, tp):
    self.x = x
    self.y = y
    self.tp = tp
    self.dis = int(sqrt((x - Yolowidth / 2)**2 + (y - Yolowidth / 2)**2))

  def __lt__(self, other):

    s = self.dis * (1 if 'h' in self.tp else 10000)
    o = other.dis * (1 if 'h' in self.tp else 10000)
    return s < o

  def disok(self):
    if self.dis < 40:
      return True
    return False


def pdetections(detections):

  for detection in detections:
    if float(detection[1]) < 0.5:
      continue
    x, y, w, h = detection[2][0],\
        detection[2][1],\
        detection[2][2],\
        detection[2][3]
    xmin, ymin, xmax, ymax = convertBack(
        float(x), float(y), float(w), float(h))
    if 'h' in detection[0].decode():
      sxmin = xmin
      sxmax = xmax
      symin = ymin
      symax = ymax
    else:
      sxmin = int(0.1 * w) + xmin
      sxmax = int(0.9 * w) + xmin
      symin = ymin
      symax = int(0.6 * h) + ymin
    if sxmin < Yolowidth / 2 and sxmax > Yolowidth / 2 and symin < Yolowidth / 2 and symax > Yolowidth / 2:
      print("START SHOT", sxmin, symin, sxmax, symax)
      aimbot.shot(0, 0)
      return


def head(detections):

  ar = []
  for detection in detections:
    if float(detection[1]) < 0.5:
      continue
    x, y, w, h = detection[2][0],\
        detection[2][1],\
        detection[2][2],\
        detection[2][3]
    xmin, ymin, xmax, ymax = convertBack(
        float(x), float(y), float(w), float(h))
    tp = detection[0].decode()
    if 'h' in tp:
      ar.append(Arec(random.randint(
          xmin, xmax
      ), random.randint(ymin, ymax), tp))
    else:
      sx = int(random.randint(2, 6) * 0.1 * w) + xmin
      sy = int(random.randint(1, 5) * 0.1 * h) + ymin
      ar.append(Arec(sx, sy, tp))

  if len(ar) > 0 and aimbot.BoolShot(600):
    ar.sort()
    for i in ar:
      print(i.x, i.y, i.dis, i.tp, i.disok())
    if ar[0].disok():
      aimbot.shot(ar[0].x, ar[0].y)
  # exit()


def Detect():
  global detections
  darknet_image = darknet.make_image(darknet.network_width(netMain),
                                     darknet.network_height(netMain), 3)
  i = 0
  while True:
    prev_time = time.time()
    i += 1
    if i % 1000 == 0:
      i = 0
      print('averge {}ms'.format(int(1000 * (time.time() - prev_time)) / 1000))
      prev_time = time.time()

    st = np.array(sct.grab(monitor))
    stime = time.time()
    frame_rgb = cv2.cvtColor(st, cv2.COLOR_BGR2RGB)

    frame_resized = cv2.resize(frame_rgb,
                               (darknet.network_width(netMain),
                                darknet.network_height(netMain)),
                               interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())

    detections = darknet.detect_image(
        netMain, metaMain, darknet_image, thresh=0.25)
    image = cvDrawBoxes(detections, frame_resized,
                        1 / (time.time() - prev_time))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    cv2.imshow('Demo', image)
    cv2.waitKey(3)
    if win32api.GetKeyState(0x14) == 1 and len(detections) > 0:
      pdetections(detections)
    # send.send(detections)


sct = mss.mss()

if __name__ == "__main__":
  # thread_monitorkeyboard = threading.Thread(target=pdetections)
  # thread_monitorkeyboard.daemon = True
  # thread_monitorkeyboard.start()
  # recv, send = Pipe(duplex=False)
  # shot = Process(target=pdetections, args=(recv,))
  # shot.daemon = True
  # shot.start()
  # zx = int(input())
  # zy = int(input())
  zx = 960
  zy = 540
  monitor['left'] = zx - int(Yolowidth / 2)
  monitor['top'] = zy - int(Yolowidth / 2)
  monitor['width'] = Yolowidth
  monitor['height'] = Yolowidth

  print(monitor)
  init()
  Detect()
  print("sb")
