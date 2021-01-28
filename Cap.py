import mss
import time
import datetime
import os
from PIL import Image
path = os.path.join('data', 'modelhead', 'fbi')
sct = mss.mss()
monitor = {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
now = datetime.datetime.now()
flist = os.listdir(path)
i = 0
while True:
  i += 1
  st = sct.grab(monitor)
  img = Image.frombytes("RGB", st.size, st.bgra, "raw", "BGRX")
  while "{}_{}_{}_{}.jpg".format(now.year, now.month, now.day, i) in flist:
    i += 1
  fn = "{}_{}_{}_{}.jpg".format(now.year, now.month, now.day, i)
  img.save(path + '/' + fn, quality=100, subsampling=0)
  time.sleep(0.5)
