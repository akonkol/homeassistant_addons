# Modified https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage
import time
import subprocess

# from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import Adafruit_SSD1306

# Thanks SO https://stackoverflow.com/questions/4048651/function-to-convert-seconds-into-minutes-hours-and-days
def display_time(seconds, granularity=2):
  INTERVALS = (
      ('w', 604800),  # 60 * 60 * 24 * 7
      ('d', 86400),    # 60 * 60 * 24
      ('h', 3600),    # 60 * 60
      ('m', 60),
      ('s', 1),
  )
  result = []
  for name, count in INTERVALS:
      value = seconds // count
      if value:
          seconds -= value * count
          result.append("{}{}".format(round(value), name))
  return ''.join(result[:granularity])

def display_stats():
  # i2c = busio.I2C(SCL, SDA)
  # disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
  RST=None
  disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
  
  # Clear display.
  disp.fill(0)
  disp.show()
  
  # Create blank image for drawing.
  # Make sure to create image with mode '1' for 1-bit color.
  width = disp.width
  height = disp.height
  image = Image.new("1", (width, height))
  
  # Get drawing object to draw on image.
  draw = ImageDraw.Draw(image)
  
  # Draw a black filled box to clear the image.
  draw.rectangle((0, 0, width, height), outline=0, fill=0)
  
  # Draw some shapes.
  # First define some constants to allow easy resizing of shapes.
  padding = -2
  top = padding
  bottom = height - padding
  # Move left to right keeping track of the current x position for drawing shapes.
  x = 0
  big_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 20)
  small_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 10)
  
  while True:
      # Draw a black filled box to clear the image.
      draw.rectangle((0, 0, width, height), outline=0, fill=0)
  
      # Shell scripts for system monitoring from here:
      # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
      hostname_cmd = "hostname -f | cut -d' ' -f1"
      HOSTNAME = subprocess.check_output(hostname_cmd, shell=True).decode("utf-8")
      ip_cmd = "hostname -I | cut -d' ' -f1"
      IP = subprocess.check_output(ip_cmd, shell=True).decode("utf-8")
      uptime_cmd = "cat /proc/uptime | cut -d' ' -f1"
      UPTIME = subprocess.check_output(uptime_cmd, shell=True).decode("utf-8")
      uptime_in_seconds = float(UPTIME.strip())
  
      draw.text((x, top + 0), HOSTNAME, font=big_font, fill=255)
      draw.text((x, top + 24), IP, font=small_font, fill=255)
      draw.text((width - 30 , top + 24), display_time(uptime_in_seconds, 4), font=small_font, fill=255)
  
      # Display image.
      disp.image(image)
      disp.show()
      time.sleep(0.1)

if __name__ == "__main__":
  display_stats()
