
import spidev
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#SPI Setup
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

#the chip select pin is connected to GPIO 12, depending on it the data will be read or not read
CS_ADC = 12
GPIO.setup(CS_ADC, GPIO.OUT)


def analogRead(channel):
  adc = spi.xfer2([6|(channel>>2),channel<<6,0]) # 0 0 0 0  0 1 1 D2, D1 D0 0 0  0000, 00000000
  data = ((adc[1]&15) << 8) + adc[2]

  adc_value = 3.3 * ( data / (2** 12 -1))  # vref*(value/(2**bitdepth-1))
  return data


# delay in reading data
delay = 0.5
 
while True:
  GPIO.output(CS_ADC, GPIO.LOW)
  value = analogRead(5)
  GPIO.output(CS_ADC, GPIO.HIGH)

  print(f"{value:.3f}")

  time.sleep(delay)
