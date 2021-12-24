This is a Telegram bot that can record a Google Meet meeting for you.

Commands:
 - `/join` Join a meeting
 - `/leave` Leave a meeting
 - `/start` Start recording
 - `/stop` Stop recording
 - `/kill` Kill the bot

Requirements:
 - Firefox
 - Selenium (python)
 - GStreamer (gst-launch is in gstreamer1.0-tools package iirc)
 - Pulseaudio (for Gst to record audio)
 - X11-based desktop environment (Gst uses ximagesrc)
 - `python-telegram-bot` pip package

### Usage instructions
Before you leave for school, start the bot and log in with your Google accunt in the browser window that pops up.
Disable your screensaver/screen lock so that the desktop stays alive (but prefarably turn your monitor off).
Once you have the link for the call, tell the bot to join by sending it the `/join` command. Use the other commands from there.

### Before you run it
Replace the bot token in `bot.py` with your own (ask the [Bot Father](https://t.me/botfather) to make you one).  
Change your `screen_dims` in `meet.py`.
