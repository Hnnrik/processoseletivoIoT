from machine import Pin, ADC, I2C
import dht
import time
import ssd1306
import math

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
dht_sensor =dht.DHT22(Pin(28))
gas= ADC(26) 
ldr= ADC(27)

led_azul =Pin(16, Pin.OUT)
led_amarelo = Pin(17, Pin.OUT)

led_vermelho = Pin(18, Pin.OUT)

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

while True:
    try:
        # aqui é a captação real dos sensores
        dht_sensor.measure()
        temp = dht_sensor.temperature()
 
        hum = dht_sensor.humidity()
        gas_value = gas.read_u16()
        luz = ldr.read_u16()


        t = t+0.1


        # variação dos valores para demonstração do funcionamento

        temp=25 + 20 * abs(math.sin( t))      # 25°C a 45°C 
        gas_value= int(5000 + 50000 * abs(math.sin(t/2)))  #5k a 55k 
        hum =50  +30 * abs(math.sin(t/3))     # 50% a 80%   
        luz = int(10000 +50000*abs(math.cos(t)))  # só pra preencher o senso

        if (gas_value <= 10000) or (temp <= 30): 
            estado ="NORMAL"

        if (gas_value  >10000 and gas_value<=20000 ) or (temp > 30 and temp <=35):
            estado ="ALTERACAO"

        elif (gas_value  >20000 and gas_value<=30000 ) or (temp > 35 and temp <=40):
            estado = "MEDIO" 
        
        elif (gas_value  >30000 and gas_value<=45000 ) or (temp > 40 and temp <=45):
            estado = "CRITICO"
        else:

            estado ="EXTREMO"
        

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

        oled.text("Estado:",0,45)
        oled.text(estado, 0,55)


        oled.show()

        time.sleep(1)

    except Exception as e:

        print("Erro:", e)
        time.sleep(2)