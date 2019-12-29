from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging

def hello(update, context):

    update.message.reply_text(
        "Hello {}, from :  , chat :  , message : .".format(update.message.from_user.first_name))
    context.bot.send_message(chat_id=update.message.from_user.id, text="I'm a bot, please talk to me! {} ".format(update.message.from_user.id))

def start(update, context):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1,'+str(update.effective_chat.id)),
                 InlineKeyboardButton("Option 2", callback_data='2,'+str(update.effective_chat.id))],
                [InlineKeyboardButton("Option 3", callback_data='3,'+str(update.effective_chat.id))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.message.from_user.id, text='Please choose:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    
    query.edit_message_text(text="Selected option: {}, chatid:{}".format(query.data,update.effective_chat.id))
    arg=query.data.split(',')
    context.bot.send_message(chat_id=int(arg[1]), text='choosen:{}'.format(arg[0]))


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")



updater = Updater('1043079672:AAGKrVHxXkROQTZG-T9CQ0gyjGw4hzEls5s', use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('help', help))


updater.start_polling()
updater.idle()