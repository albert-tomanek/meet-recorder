#!/usr/bin/env python3

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from os import system
import time

TOKEN = '5086791268:AAHwFvAJS_VfJD0M7n_aJpIbHoPAj99zAA8'

updater    = Updater(TOKEN)         # Fetches updates fro Telegram server
dispatcher = updater.dispatcher     # Filters updates and dispaches callbacks

def join(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')

def leave(update: Update, context: CallbackContext) -> None:
    pass

def start(update: Update, context: CallbackContext) -> None:
    pass

def stop(update: Update, context: CallbackContext) -> None:
    pass

dispatcher.add_handler(CommandHandler('join', join))
dispatcher.add_handler(CommandHandler('leave', leave))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('stop', stop))

print('Started bot.')

updater.start_polling()
updater.idle()
