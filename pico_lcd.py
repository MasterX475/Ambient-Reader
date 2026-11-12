import utime
from machine import I2C

class I2cLcd:
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = True
        self.i2c.writeto(self.i2c_addr, bytes([0x00]))
        utime.sleep_ms(20)
        self._write_init_nibble(0x30)
        utime.sleep_ms(5)
        self._write_init_nibble(0x30)
        utime.sleep_ms(1)
        self._write_init_nibble(0x30)
        self._write_init_nibble(0x20)
        self._write_cmd(0x28)
        self._write_cmd(0x0C)
        self._write_cmd(0x06)
        self.clear()

    def _write_init_nibble(self, nibble):
        byte = nibble & 0xF0
        self.i2c.writeto(self.i2c_addr, bytes([byte | 0x0C, byte | 0x08]))

    def _write_cmd(self, cmd):
        high = cmd & 0xF0
        low = (cmd << 4) & 0xF0
        self.i2c.writeto(self.i2c_addr, bytes([high | 0x0C, high | 0x08, low | 0x0C, low | 0x08]))

    def _write_data(self, data):
        high = data & 0xF0
        low = (data << 4) & 0xF0
        self.i2c.writeto(self.i2c_addr, bytes([high | 0x0D, high | 0x09, low | 0x0D, low | 0x09]))

    def clear(self):
        self._write_cmd(0x01)
        utime.sleep_ms(2)

    def move_to(self, cursor_x, cursor_y):
        addr = cursor_x & 0x3F
        if cursor_y & 1: addr += 0x40
        if cursor_y & 2: addr += self.num_columns
        self._write_cmd(0x80 | addr)

    def putstr(self, string):
        for char in string:
            self._write_data(ord(char))
