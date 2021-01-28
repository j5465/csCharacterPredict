import time
from pyclick import HumanClicker
from PIL import Image
import PressKey
import win32api
import os
import random
import mss
from math import atan, sqrt, pi, sin, cos
hc = HumanClicker()
keys = PressKey.Keys()
shooting = False
monitor = {}


def Cancelrecoil():
  global shooting
  dx = 12
  dy = 65
  dx = int(atan(4 * dx / (sqrt(3) * 1920)) * 57.3 * 25.17)
  dy = int(30 * 54 * dy / 1080)
  d = hc.Gdxdy((dx, dy))
  print(d)

  for i in range(len(d)):
    if win32api.GetKeyState(0x01) < 0:
      print(d[i])
      keys.directMouse(d[i][0], d[i][1])
      time.sleep(1 / len(d))
    else:
      break
  shooting = False


def getStime():
  startt = None
  while win32api.GetKeyState(0x01) < 0:
    if startt == None:
      startt = time.time()
    else:
      time.sleep(0.001)
  if startt != None:
    print(time.time() - startt)


def shot():
  i = 0
  sct = mss.mss()
  while win32api.GetKeyState(0x01) < 0:

    i += 1
    st = sct.grab(monitor)
    img = Image.frombytes("RGB", st.size, st.bgra, "raw", "BGRX")
    img.save(os.path.join('recoil/ak{}.jpg'.format(i)))
    time.sleep(0.05)


if __name__ == "__main__":
  actions = [[0, 0]]
  for i in range(0, 12):
    si = 5 * cos(i * pi / 6)
    cs = 5 * sin(i * pi / 6)
    actions.append([int(si), int(cs)])
  print(actions)
  # print(int(si), int(cs))
  # zx = 960
  # zy = 540
  # monitor['left'] = zx - 200
  # monitor['top'] = zy - 200
  # monitor['width'] = 400
  # monitor['height'] = 400

  # while True:
  #   if win32api.GetKeyState(0x01) < 0 and shooting == False:
  #     shooting = True
  #     Cancelrecoil()

  #   time.sleep(0.01)

# -4 7
# 4 19
# -3 29
# -1 31
# 13 31
# 8 28
# 13 21

# -17 12
# -42 - 3
# -21 2
# 12 11
# -15 7
# -26 - 8
# -3 4
# 40 1
# 19 7
# 14 10
# 27 0
# 33 - 10
# -21 - 2
# 7 3
# -7 9
# -8 4
