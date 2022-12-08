import uasyncio as asyncio
from machine import UART

class Sc08aController:
    _baudrate = 9600
    
    _MIN_ANGLE = 0
    _MAX_ANGLE = 8000
    
    _writer_created = False
    _reader_created = False

    def __init__(self, uart_id):
        self.uart = UART(uart_id, baudrate=self._baudrate)

    async def close(self):
        await self.disable_channel()
        self.uart.deinit()

    async def _write_byte(self, buffer):
        if not self._writer_created:
            self._writer_created = True
            self._writer = asyncio.StreamWriter(self.uart, {})

        self._writer.write(buffer)
        await self._writer.drain()
        await asyncio.sleep_ms(250)

    async def _read_bytes(self, len = 1):
        if not self._reader_created:
            self._reader_created = True
            self._reader = asyncio.StreamReader(self.uart)
        data = await self._reader.readline()
        return data

    async def init_controller(self, channel):
        await self._write_byte(bytes([0x81, 0x0F, 0xA0, 0x0A]))
        await self._write_byte(bytes([0x82, 0x0F, 0xA0, 0x0A]))
        
    async def enable_channel(self):
        await self._write_byte(bytes([0xC0, 0x01, 0x0A]))
        
    async def disable_channel(self):
        await self._write_byte(bytes([0xC0, 0x00, 0x0A]))

    async def set_position_with_speed(self, position, speed, channel):
        first_byte = 0b11100000 | channel
        high_byte = (position >> 6) & 0b01111111
        low_byte = position & 0b00111111
        speed_byte = 0b00000000 | speed
        await self._write_byte(bytes([first_byte, high_byte, low_byte, speed_byte, 0x0A]))

    async def set_angle(self, angle, speed, channel):
        if angle < -90 or angle > 90:
            return False
        
        position = (angle + 90) * (self._MAX_ANGLE - self._MIN_ANGLE) / 180
        position = int(position)
        await self.set_position_with_speed(position, speed, channel)

    async def get_position(self):
        data = await self._read_bytes()
        return data