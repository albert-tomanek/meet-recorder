#!/usr/bin/env python3

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from meet import MeetRecorder

from os import system
import time

TOKEN = '5086791268:AAHwFvAJS_VfJD0M7n_aJpIbHoPAj99zAA8'

updater    = Updater(TOKEN)         # Fetches updates fro Telegram server
dispatcher = updater.dispatcher     # Filters updates and dispaches callbacks

def join(update: Update, context: CallbackContext) -> None:
    meet.join('https://meet.google.com/jzd-xidq-nme')

def leave(update: Update, context: CallbackContext) -> None:
    meet.leave()

def start(update: Update, context: CallbackContext) -> None:
    pass

def stop(update: Update, context: CallbackContext) -> None:
    pass

def kill(update: Update, context: CallbackContext) -> None:
    del meet

dispatcher.add_handler(CommandHandler('join', join))
dispatcher.add_handler(CommandHandler('leave', leave))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('stop', stop))

dispatcher.add_handler(CommandHandler('kill', kill))

# Initialize bot

meet = MeetRecorder()

print('\nStarted bot.')

updater.start_polling()
updater.idle()
