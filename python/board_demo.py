import board as b
import time

b.init()
b.homeOff()

b.allOn()
time.sleep(1)
b.homeOff()
time.sleep(1)
b.allOn()
time.sleep(1)
b.homeOff()

for a in range(1,10):
    b.on(b.HOME_BOTTOM_LEFT)
    time.sleep(0.1)
    b.off(b.HOME_BOTTOM_LEFT)
    b.on(b.HOME_TOP_LEFT)
    time.sleep(0.1)
    b.off(b.HOME_TOP_LEFT)
    b.on(b.HOME_TOP)
    time.sleep(0.1)
    b.off(b.HOME_TOP)
    b.on(b.HOME_TOP_RIGHT)
    time.sleep(0.1)
    b.off(b.HOME_TOP_RIGHT)
    b.on(b.HOME_BOTTOM_RIGHT)
    time.sleep(0.1)
    b.off(b.HOME_BOTTOM_RIGHT)
    b.on(b.HOME_BOTTOM)
    time.sleep(0.1)
    b.off(b.HOME_BOTTOM)

b.homeOff()
b.awayOff()

