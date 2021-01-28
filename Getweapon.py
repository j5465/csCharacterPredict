import mss
import time
import numpy as np
import cv2
import os
from PIL import Image

wpath = os.path.join('weapon')
dirlist = os.listdir(wpath)
monitor = {'zhu': {'left': 1850, 'top': 837, 'width': 40, 'height': 14},
           'fu': {'left': 1830, 'top': 920, 'width': 61, 'height': 17}}
mdimg = {'zhu': ['ak47.jpg', 'awp.jpg', 'm4a4.jpg'], 'fu': ['shamo.jpg']}
sct = mss.mss()


def generate_weapon_txt(wdir, wtype):

  imglist = os.listdir(wpath + '/{}'.format(wdir))
  cutedimg = []
  for img in imglist:
    if img.endswith('.jpg') == False:
      continue
    yimg = Image.open(wpath + '/{}/{}'.format(wdir, img))
    if yimg.mode in ('RGBA', 'P'):
      yimg = yimg.convert('RGB')

    cutedimg.append(yimg.convert('L'))
    # ret, thresh1=cv2.threshold(GrayImage, 200, 255, cv2.THRESH_BINARY)
  print(len(cutedimg))
  scount = 0
  width, height = cutedimg[0].size
  print(width, height)
  sbimg = Image.new("L", (width, height), color=0)

  for x in range(width):
    for y in range(height):
      color = cutedimg[0].getpixel((x, y)) > 150
      # print(x, y, color)
      same = True
      for i in range(1, len(cutedimg)):
        irgb = cutedimg[i].getpixel((x, y)) > 150
        # print(x, y, color, irgb)
        if irgb != color:
          same = False
          break

      if same:
        # print('same', x, y)
        sbimg.putpixel((x, y), 255)
        scount += 1

  print(scount)
  sbimg.save('{}/{}.jpg'.format(wpath, wdir))


def Cap(wname, wtype):
  i = 0
  while True:
    i += 1
    st = sct.grab(monitor[wtype])
    img = Image.frombytes("RGB", st.size, st.bgra, "raw", "BGRX")
    while os.path.exists('{}/{}/{}.jpg'.format(wpath, wname, i)):
      i += 1
    img.save('{}/{}/{}.jpg'.format(wpath, wname, i))
    time.sleep(0.5)


def detectWeapon():

  for m in monitor:
    st = sct.grab(monitor[m])
    img = Image.frombytes("RGB", st.size, st.bgra, "raw", "BGRX")
    img = img.convert('L')
    for wp in mdimg[m]:
      Mbimg = Image.open(wpath + '/{}'.format(wp))
      width, height = Mbimg.size
      hd, match, zbds = 0, 0, 0

      for x in range(width):
        for y in range(height):
          clw = img.getpixel((x, y)) > 150
          mclw = Mbimg.getpixel((x, y)) > 150
          if mclw:
            zbds += 1
          if clw and mclw:
            match += 1
          else:
            hd += 1
      if hd > int(0.5 * width * height) and match == zbds:
        # print(hd, match, zbds, width, height)
        print(wp.split('.')[0])
        return wp.split('.')[0]
  return 'ak47'

# detectWeapon()
# generate_weapon_txt('shamo', 'fu')
# generate_weapon_txt('ak47', 'zhu')
# generate_weapon_txt('ak47', 'zhu')
# generate_weapon_txt('m4a4', 'zhu')
# Cap('m4a4')
