# rpi-lastfm-playing-screen
A script to display on the Pimoroni OLED ic2 screen what you are actually scrobbling.

The screen used : https://shop.pimoroni.com/products/1-12-oled-breakout?variant=12628508704851

# Features
This script can read the LAST.FM API to know what are you listening right now, and write the "Artist - Track" on the screen.
When the script detects that you aren't listening to something, it displays an "Offline ..." message with the number of your total scrobbles.

As soon as we listening again to something, the screen "wakes up" and show the current time and the "Artist - Track".

# My setup for this project

- A Raspberry PI Zero W
- Updated Raspbian distro
- An internet connection (to connects by SSH, to install/update packages and for the LastFM API)
- Python 3 (Python 2 will work too, normally)
- The pimoroni screen : https://shop.pimoroni.com/products/1-12-oled-breakout?variant=12628508704851
- The Breakout garden mini : https://shop.pimoroni.com/products/breakout-garden-mini-i2c-spi

# How to use it

blablabla (to write)
