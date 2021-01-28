from time import sleep
import win32gui


while True:
  sleep(0.1)
  int_x = win32gui.GetCursorPos()[0]
  int_y = win32gui.GetCursorPos()[1]
  print(int_x, int_y)
