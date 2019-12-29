#   External Import
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def getButtonCallBackData(query):
    arg = query.data.split(',')
    return arg[0], int(arg[1]), int(arg[2]), int(arg[3]), arg[4]


def createButtonMarkup(textList, callbackKey, chatid):
    keyboard = []
    for i in range(len(textList)):
        keyboard.append([])
        for i2 in range(len(textList[i])):
            keyboard[i].append(InlineKeyboardButton(textList[i][i2],
                                                    callback_data="{},{},{},{},{}".format(callbackKey, chatid, i, i2,
                                                                                          textList[i][i2])))
    return InlineKeyboardMarkup(keyboard)


def sendButton(context, update, targetChatId, queryText, callBackKey, buttonList):
    reply_markup = createButtonMarkup(buttonList,callBackKey,str(update.effective_chat.id))
    context.bot.send_message(chat_id=targetChatId,
                             text=queryText,
                             reply_markup=reply_markup)


def List2String(liststring):
    s = ""
    for i in liststring:
        s = s + str(i) + "\n"
    return s