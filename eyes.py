import uasyncio as asyncio
from eye import Eye
from sc08a import Sc08aController

class EyesControl:
    _left_eye = Eye(0, 128, 64, 8, 9)
    _right_eye = Eye(1, 128, 64, 6, 7)
    _controller = Sc08aController(1)
    _speed = 0

    async def _play(self, eye):
        await eye.blink(10)
        await eye.clear()

    async def _sender(self, controller, speed):
        await controller.enable_channel()
        await controller.set_angle(-15, speed, 1)
        await controller.set_angle(0, speed, 2)
        await controller.set_angle(-45, speed, 1)
        await controller.set_angle(-15, speed, 1)
        await controller.set_angle(45, speed, 1)
        await controller.set_angle(-15, speed, 1)
        await controller.set_angle(-45, speed, 2)
        await controller.set_angle(-5, speed, 2)
        await controller.set_angle(45, speed, 2)
        await controller.set_angle(0, speed, 2)
        await controller.close()

    async def run(self, e):
        if e == 0:
            await self._sender(self._controller, self._speed)
        elif e == 1:
            await self._play(self._left_eye)
        else:
            await self._play(self._right_eye)
