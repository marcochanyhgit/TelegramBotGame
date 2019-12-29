from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging
# ----- Tools ----- #
def getButtonCallBackData(query):
    arg=query.data.split(',')
    return arg[0],int(arg[1]),int(arg[2]),int(arg[3]),arg[4]

def createButtonMarkup(textList,callbackKey,chatid):
    keyboard=[]
    for i in range(len(textList)):
        keyboard.append([])
        for i2 in range(len(textList[i])):
            keyboard[i].append(InlineKeyboardButton(textList[i][i2],callback_data="{},{},{},{},{}".format(callbackKey,chatid,i,i2,textList[i][i2])))
    return InlineKeyboardMarkup(keyboard)

def sendButton(context,update,targetChatId,queryText,callBackKey,buttonList):
    reply_markup=createButtonMarkup(buttonList,callBackKey,str(update.effective_chat.id))
    context.bot.send_message(chat_id=targetChatId, text=queryText, reply_markup=reply_markup)
    
# ----- Game Logic ----- #

# ----- Commands ----- #

def start(update, context):
    sendButton(context,update,update.message.from_user.id,"Choose Game","ChooseGame",[["Dead Man's Draw","Option 2"],["Option 3"]])


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")

# ----- Call back handler ----- #
def button_callBack(update, context):
    query = update.callback_query
    callBackKey,chatid,posY,posX,content=getButtonCallBackData(query)
    query.edit_message_text(text="Selected : {}".format(content))
    context.bot.send_message(chat_id=chatid, text='choosen:{},{},{}'.format(content,posY,posX))


# ----- Startup calls ----- #
updater = Updater('1043079672:AAGKrVHxXkROQTZG-T9CQ0gyjGw4hzEls5s', use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button_callBack))
updater.dispatcher.add_handler(CommandHandler('help', help))


updater.start_polling()
updater.idle()