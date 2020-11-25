# LastFm-OLED-Stats
A script to display on the Pimoroni OLED SPI screen what you are actually scrobbling.

The screen used : https://shop.pimoroni.com/products/1-12-oled-breakout?variant=12628508704851

# Features
This script can read the LAST.FM API to know what are you listening right now, and write the "Artist - Track" on the screen.
When the script detects that you aren't listening to something, it displays an "Offline ..." message with the number of your total scrobbles.

As soon as we listening again to something, the screen "wakes up" and show the current time and the "Artist - Track".

# My setup for this project

- A Raspberry PI Zero W
- Updated Raspbian distro
- An internet connection (to connects by SSH, to install/update packages and for the LastFM API)
- Python 3 (Python 2 will work too, normally, i think)
- The Pimoroni OLED 1.12" mini screen
- The Pimoroni Breakout garden mini

# Prerequisites

- Raspberry Pi Zero W : https://buyzero.de/collections/raspberry-pi-zero-kits/products/raspberry-pi-zero-w?variant=38399156114
- Pimoroni screen : https://shop.pimoroni.com/products/1-12-oled-breakout?variant=12628508704851
- Pimoroni Breakout  : https://shop.pimoroni.com/products/breakout-garden-mini-i2c-spi
- Python3 installed (apt install python3)
- PIP3 installed (pip3 install --upgrade pip)
- Luma installed (pip3 install luma.core)

# How to use it

1. Download the "LastFmOLED" folder
2. CD into the folder
3. Launch the python script with this command :
```
python3 /LastFmOLED/LastFmOLED.py --display sh1106 --height 128 --rotate 2 --interface spi --gpio-data-command 9 --spi-device 1
```
