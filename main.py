import uasyncio as asyncio
from eyes import EyesControl
from head import HeadControl

async def main():
    eye_control = EyesControl()
    asyncio.create_task(eye_control.run(0))
    asyncio.create_task(eye_control.run(1))
    asyncio.create_task(eye_control.run(2))
    while True:
        await asyncio.sleep_ms(50)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Interrupted.')
finally:
    asyncio.new_event_loop()