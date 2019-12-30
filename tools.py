#   External Import
from functools import wraps
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

#   Internal Import
from settings import gameData,game


def getButtonCallBackData(query):
    arg = query.data.split(',')
    return arg[0], int(arg[1]), int(arg[2]), int(arg[3]), arg[4]


def createButtonMarkup(textList, callbackKey, chatid):
    """
    :param textList:    list of text which button to play
    :param callbackKey: text of button
    :param chatid:      channel chat id
    :return:
    """
    keyboard = []
    for i in range(len(textList)):
        keyboard.append([])
        for i2 in range(len(textList[i])):
            keyboard[i].append(InlineKeyboardButton(textList[i][i2],
                                                    callback_data="{},{},{},{},{}".format(callbackKey, chatid, i, i2,
                                                                                          textList[i][i2])))
    return InlineKeyboardMarkup(keyboard)


def sendButton(context, update, targetChatId, queryText, callBackKey, buttonList):
    """
    :param context:      context of the chat
    :param update:       object storing chat message and channel id
    :param targetChatId: target id send to
    :param queryText:    display text on button
    :param callBackKey:  return text after click the button
    :param buttonList:   button list including button text
    :return:
    """
    reply_markup = createButtonMarkup(buttonList,callBackKey,str(update.effective_chat.id))
    context.bot.send_message(chat_id=targetChatId,
                             text=queryText,
                             reply_markup=reply_markup)


def List2String(liststring):
    s = ""
    for i in liststring:
        s = s + str(i) + "\n"
    return s


"""
Validation
"""
def localUserRequired(fun):
    @wraps(fun)
    def wrapper(obj,update, context, chatid, posY, posX, content, fromid):
        if (fromid != gameData[str(chatid)]["JoinList"][gameData[str(chatid)]["CurrentPlayer"]]):
            return False,""
        return fun(obj,update, context, chatid, posY, posX, content, fromid)
    return wrapper