from machine import Pin, ADC, I2C
import dht
import time
import math
from micropython import const
import framebuf

# ---------- Definição da classe SSD1306_I2C (sem import externo) ----------
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xa4)
SET_NORM_INV = const(0xa6)
SET_DISP = const(0xae)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xa0)
SET_MUX_RATIO = const(0xa8)
SET_COM_OUT_DIR = const(0xc0)
SET_DISP_OFFSET = const(0xd3)
SET_COM_PIN_CFG = const(0xda)
SET_DISP_CLK_DIV = const(0xd5)
SET_PRECHARGE = const(0xd9)
SET_VCOM_DESEL = const(0xdb)
SET_CHARGE_PUMP = const(0x8d)

class SSD1306_I2C:
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.buffer = bytearray(self.height // 8 * self.width)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([0x80, cmd]))

    def write_data(self, buf):
        self.i2c.writeto(self.addr, b'\x40' + buf)

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00,
            SET_MEM_ADDR, 0x00,
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08,
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x12,
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0xf1,
            SET_VCOM_DESEL, 0x30,
            SET_CONTRAST, 0xff,
            SET_ENTIRE_ON,
            SET_NORM_INV,
            SET_CHARGE_PUMP, 0x14,
            SET_DISP | 0x01,
        ):
            self.write_cmd(cmd)

    def fill(self, col):
        self.framebuf.fill(col)

    def text(self, string, x, y):
        self.framebuf.text(string, x, y)

    def show(self):
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.width - 1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.height // 8 - 1)
        self.write_data(self.buffer)


i2c = I2C(0, scl=Pin(19), sda=Pin(18))
oled = SSD1306_I2C(128, 64, i2c)   

dht_sensor = dht.DHT22(Pin(4))

gas = ADC(Pin(34))   
ldr = ADC(Pin(35))  

led_azul = Pin(15, Pin.OUT)
led_amarelo = Pin(16, Pin.OUT)
led_vermelho = Pin(17, Pin.OUT)

def apagar_todos():
    led_azul.off()
    led_amarelo.off()
    led_vermelho.off()

def piscar(led, tempo=0.3):
    led.on()
    time.sleep(tempo)
    led.off()
    time.sleep(tempo)

t = 0

for i in range(0,5):
    try:
        
        t = t + 0.4
        temp = 25 + 20 * abs(math.sin(t))
        gas_value = int(5000 + 50000 * abs(math.sin(t/2)))
        hum = 50 + 30 * abs(math.sin(t/3))
        luz = int(10000 + 50000 * abs(math.cos(t)))

        if (gas_value <= 10000) or (temp <= 30):
            estado = "NORMAL"
        if (gas_value > 10000 and gas_value <= 20000) or (temp > 30 and temp <= 35):
            estado = "ALTERACAO"
        elif (gas_value > 20000 and gas_value <= 30000) or (temp > 35 and temp <= 40):
            estado = "MEDIO"
        elif (gas_value > 30000 and gas_value <= 45000) or (temp > 40 and temp <= 45):
            estado = "CRITICO"
        else:
            estado = "EXTREMO"

        apagar_todos()
        if estado == "NORMAL":
            led_azul.on()
        elif estado == "ALTERACAO":
            led_azul.on()
            piscar(led_amarelo)
        elif estado == "MEDIO":
            led_amarelo.on()
        elif estado == "CRITICO":
            led_amarelo.on()
            piscar(led_vermelho)
        elif estado == "EXTREMO":
            led_vermelho.on()

        oled.fill(0)
        oled.text("Temp: {}C".format(temp), 0, 0)
        oled.text("Hum:{}%".format(hum), 0, 10)
        oled.text("Gas:{}".format(gas_value), 0, 20)
        oled.text("Luz:{}".format(luz), 0, 30)
        oled.text("Estado:", 0, 45)
        oled.text(estado, 0, 55)
        oled.show()

        time.sleep(0.4)


    except Exception as e:
        print("Erro:", e)
        time.sleep(2)
print("Teste")