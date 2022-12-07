#from eyes import Eyes
from sc08a import Sc08aController
from time import sleep
import uasyncio as asyncio

#e = Eyes(128, 64, 8, 9)
#e.blink(5)
#e.clear()

controller = Sc08aController(1)

async def sender(h, s):
    await h.enable_channel()
    await h.set_angle(0, s, 1)
    await h.set_angle(0, s, 2)
    await h.set_angle(-90, s, 1)
    await h.set_angle(0, s, 1)
    await h.set_angle(90, s, 1)
    await h.set_angle(0, s, 1)
    await h.set_angle(-90, s, 2)
    await h.set_angle(0, s, 2)
    await h.set_angle(90, s, 2)
    await h.set_angle(0, s, 2)
    await h.close()

async def main():
    asyncio.create_task(sender(controller, 0))
    while True:
        await asyncio.sleep(1)

def test():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()

test()
