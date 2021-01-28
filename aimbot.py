from pyclick import HumanClicker
import time
import PressKey
import numpy as np
import threading
import win32api
import win32gui
from math import atan, sqrt
import Getweapon
import random
import ctypes
# import json
hc = HumanClicker()
keys = PressKey.Keys()
Press = {}
mlist = ['W', 'S', 'A', 'D']
shotflag = False
delaytype = {'mouseclick': (120, 30), 'jt': (100, 20), 'fire': (250, 50)}
lastshot = time.time()
Yolowidth = 288

# mp = {}
# with open("mp.txt", 'r') as f:
#   mp = json.loads(f.read())


def BoolShot(ms):
  global lastshot
  nt = time.time()
  if int(1000 * (nt - lastshot)) > ms:
    return True
  return False

# H:1/30*H==54
# X 1o = 22.17


def moveMouse(x, y):

  GHeight = 1080
  GWidth = 1920
  dx = x - Yolowidth / 2
  dy = y - Yolowidth / 2
  # print('moveMouse:', dx, dy)

  dx = int(atan(4 * dx / (sqrt(3) * GWidth)) * 57.3 * 25.17)
  dy = int(30 * 54 * dy / GHeight)
  # print('moveMouse:', dx, dy)

  d = hc.Gdxdy((dx, dy))
  try:
    for dxy in d:
      # keys.directMouse(int(2.4 * dxy[0]), int(2.4 * dxy[1]))
      keys.directMouse(dxy[0], dxy[1])
      # zdx -= mp['{} {}'.format(abs(dxy[0]), abs(dxy[1]))][0]
      # zdy -= mp['{} {}'.format(abs(dxy[0]), abs(dxy[1]))][1]
      time.sleep(random.randint(6, 10) * 0.001)
    # print("zd:", zdx, zdy)
    # keys.directMouse(zdx, zdy)
  except Exception as e:
    print(e)


def mouseclick(isL):
  keys.directMouse(buttons=keys.mouse_lb_press if isL else keys.mouse_rb_press)
  time.sleep(0.001 * int(np.random.normal(delaytype['mouseclick'], 1)[0]))
  keys.directMouse(
      buttons=keys.mouse_lb_release if isL else keys.mouse_rb_release)


def keyboardclick(key, dt):
  keys.directKey(key)
  time.sleep(0.001 * int(np.random.normal(delaytype[dt], 1)[0]))
  keys.directKey(key, keys.key_release)


def getPress():
  for key in mlist:
    # Press[key] = win32api.GetAsyncKeyState(ord(key)) < 0
    Press[key] = win32api.GetKeyState(ord(key)) < 0


def jt():
  # if Press['shift'] or Press['ctrl']:
    # return
  global Press
  getPress()
  standing = True
  for ori in mlist:
    if Press[ori]:
      standing = False
      ctypes.windll.user32.RegisterHotKey(
          None, mlist.index(ori), None, ord(ori))
      keys.directKey(ori, keys.key_release)

  if Press['W']:
    if Press['S']:
      pass
    else:
      keyboardclick('S', 'jt')
  elif Press['S']:
    if Press['W']:
      pass
    else:
      keyboardclick('W', 'jt')
  elif Press['A']:
    if Press['D']:
      pass
    else:
      keyboardclick('D', 'jt')
  elif Press['D']:
    if Press['A']:
      pass
    else:
      keyboardclick('A', 'jt')
  return standing


def shot(x, y):
  jt()
  # moveMouse(x, y)

  mouseclick(isL=True)
  global lastshot, Press
  lastshot = time.time()
  # time.sleep(1)

  for ori in mlist:
    if Press[ori]:
      ctypes.windll.user32.UnregisterHotKey(None, mlist.index(ori))


if __name__ == "__main__":
  time.sleep(1)
  keys.directMouse(0, 200)
  # time.sleep(2)
  # keys.directMouse(-300, -300)

# 7980
# 389 349
# 50 25
# 100 50
