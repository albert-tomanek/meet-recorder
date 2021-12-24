This is a Telegram bot that can record a Google Meet meeting for you.

Requirements:
 - Firefox
 - Selenium (python)
 - GStreamer (gst-launch is in gstreamer1.0-tools package iirc)
 - Pulseaudio (for Gst to record audio)
 - X11-based desktop environment (Gst uses ximagesrc)
 - `python-telegram-bot` pip package

Off-screen rendering would be too complicated to do, so your computer needs to be running with its screen on when you're out and about for this to work. 


