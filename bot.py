#!/usr/bin/env python3

from telegram import Update
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CallbackContext
from telegram.ext.filters import Filters

from meet import MeetRecorder, NotAMeetLinkException

from os import system
import time

TOKEN = '5086791268:AAHwFvAJS_VfJD0M7n_aJpIbHoPAj99zAA8'

updater    = Updater(TOKEN)         # Fetches updates fro Telegram server
dispatcher = updater.dispatcher     # Filters updates and dispaches callbacks

def join(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Paste the Google Meet link.')
    return 'requested-link'

def on_received_meet_link(update: Update, context: CallbackContext) -> None:
    try:
        meet.join(update.effective_message.text)
        update.message.reply_text('Joined meeting.')
    except NotAMeetLinkException:
        update.message.reply_text("That's not a Google Meet link. 👎")
    return ConversationHandler.END

def leave(update: Update, context: CallbackContext) -> None:
    meet.leave()

def start(update: Update, context: CallbackContext) -> None:
    meet.start(str(int(time.time())) + '.ogg')

def stop(update: Update, context: CallbackContext) -> None:
    meet.stop()

def kill(update: Update, context: CallbackContext) -> None:
    quit()

dispatcher.add_handler(ConversationHandler(
    entry_points=[
        CommandHandler('join', join)
    ],
    states={
        'requested-link': [MessageHandler(Filters.text, on_received_meet_link)],
    },
    fallbacks=[]
))
dispatcher.add_handler(CommandHandler('leave', leave))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('stop', stop))

dispatcher.add_handler(CommandHandler('kill', kill))

# Initialize bot

meet = MeetRecorder()

print('\nStarted bot.')

updater.start_polling()
updater.idle()
