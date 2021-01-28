import pyautogui
import time
import threading
from pynput import keyboard
ucode = keyboard.KeyCode(char="u")
fc = False


def fuckclick():
  global fc
  while True:
    if fc:
      pyautogui.click()
    time.sleep(0.05)


def on_release(key):
  # print("{0} released".format(key), type(key))

  if key == ucode:
    print("shit")
    global fc
    fc = True
    # fuckclick()


def on_press(key):

  if key == keyboard.Key.esc:
    global fc
    fc = False
    # exit()
    # Stop listen
    # return False


thread_monitorkeyboard = threading.Thread(target=fuckclick)
thread_monitorkeyboard.daemon = True
thread_monitorkeyboard.start()
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
  listener.join()
