import pyautogui
from pyclick.humancurve import HumanCurve
from math import sqrt


def setup_pyautogui():
  # Any duration less than this is rounded to 0.0 to instantly move the mouse.
  pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
  # Minimal number of seconds to sleep between mouse moves.
  pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
  # The number of seconds to pause after EVERY public function call.
  pyautogui.PAUSE = 0.015  # Default: 0.1


setup_pyautogui()


class HumanClicker():
  def __init__(self):
    pass

  def Gdxdy(self, toPoint, humanCurve=None):
    fromPoint = (0, 0)
    dis = int(sqrt(toPoint[0] * toPoint[0] +
                   toPoint[1]  * toPoint[1]) )
    duration = int(dis * 0.5)  # ms
    pointscount = max(3, int(duration / 8))
    # print(dis, duration, pointscount)
    if not humanCurve:
      humanCurve = HumanCurve(fromPoint, toPoint, targetPoints=pointscount)
    d = []
    # print(humanCurve.points)
    yx, yy = 0, 0
    for i in range(1, len(humanCurve.points)):
      dx, dy = int(humanCurve.points[i][0] -
                   yx), int(humanCurve.points[i][1] - yy)

      d.append((dx, dy))
      yx += dx
      yy += dy

    # print(humanCurve.points)
    # print(d)
    return d

  def click(self):
    # pyautogui.PAUSE = 3
    pyautogui.click()
