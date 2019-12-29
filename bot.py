from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging

def hello(update, context):

    update.message.reply_text(
        "Hello {}, from :  , chat :  , message : .".format(update.message.from_user.first_name))
    context.bot.send_message(chat_id=update.message.from_user.id, text="I'm a bot, please talk to me! {} ".format(update.message.from_user.id))

def createButtonMarkup(textList,callbackKey,chatid):
    keyboard=[]
    for i in range(len(textList)):
        keyboard.append([])
        for i2 in range(len(textList[i])):
            keyboard[i].append(InlineKeyboardButton(textList[i][i2],callback_data="{},{},{},{}".format(callbackKey,chatid,i,i2)))
    return InlineKeyboardMarkup(keyboard)



def sendButton(context,update,targetChatId,queryText,callBackKey,buttonList):
    reply_markup=createButtonMarkup(buttonList,callBackKey,str(update.effective_chat.id))
    context.bot.send_message(chat_id=targetChatId, text=queryText, reply_markup=reply_markup)

def start(update, context):
    sendButton(context,update,update.message.from_user.id,"Choose Game","ChooseGame",[["Dead Man's Draw","Option 2"],["Option 3"]])


def button(update, context):
    query = update.callback_query
    
    query.edit_message_text(text="Selected option: {}, chatid:{}".format(query.data,update.effective_chat.id))
    arg=query.data.split(',')
    context.bot.send_message(chat_id=int(arg[1]), text='choosen:{},{},{}'.format(arg[0],arg[2],arg[3]))


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")



updater = Updater('1043079672:AAGKrVHxXkROQTZG-T9CQ0gyjGw4hzEls5s', use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('help', help))


updater.start_polling()
updater.idle()