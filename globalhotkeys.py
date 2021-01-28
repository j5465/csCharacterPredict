import os
import sys
import ctypes
import time
from ctypes import wintypes
import win32con
import win32api
byref = ctypes.byref
user32 = ctypes.windll.user32
# print(win32api.GetKeyboardState())


HOTKEYS = {
    0: ord('W'),
    1: ord('S'),
    2: ord('A'),
    3: ord('D'),


}


def handle_win_f3():
  print("sb")


def handle_win_f4():
  user32.PostQuitMessage(0)


HOTKEY_ACTIONS = {
    1: handle_win_f3,
    2: handle_win_f4
}

#
# RegisterHotKey takes:
#  Window handle for WM_HOTKEY messages (None = this thread)
#  arbitrary id unique within the thread
#  modifiers (MOD_SHIFT, MOD_ALT, MOD_CONTROL, MOD_WIN)
#  VK code (either ord ('x') or one of win32con.VK_*)
#
for id, k in HOTKEYS.items():

  print("Registering id", id, "for key", k)
  if not user32.RegisterHotKey(None, id, None, k):
    print("Unable to register id", id)

time.sleep(10)


# try:
#   msg = wintypes.MSG()
#   while user32.GetMessageA(byref(msg), None, 0, 0) != 0:
#     print(msg.message, msg.lParam, msg.time, msg.pt)
#     if msg.message == win32con.WM_HOTKEY:

#       print(msg.wParam)
#     user32.TranslateMessage(byref(msg))
#     user32.DispatchMessageA(byref(msg))

# finally:
#   for id in HOTKEYS.keys():
#     user32.UnregisterHotKey(None, id)
