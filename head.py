from sc08a import Sc08aController
import uasyncio as asyncio

class HeadControl:
    _controller = Sc08aController(1)
    _speed = 0

    async def _sender(self, controller, speed):
        await controller.enable_channel()
        await controller.set_angle(-15, speed, 1)
        await controller.set_angle(0, speed, 2)
        await controller.set_angle(-90, speed, 1)
        await controller.set_angle(-15, speed, 1)
        await controller.set_angle(90, speed, 1)
        await controller.set_angle(-15, speed, 1)
        await controller.set_angle(-90, speed, 2)
        await controller.set_angle(-5, speed, 2)
        await controller.set_angle(90, speed, 2)
        await controller.set_angle(0, speed, 2)
        await controller.close()

    async def run(self):
        await self._sender(self._controller, self._speed)