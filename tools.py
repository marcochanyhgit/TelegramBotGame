#   External Import
from functools import wraps
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

#   Internal Import
from PlayerCardDeck import PlayerCardDeck
from settings import gameData, game, CardListType


def getButtonCallBackData(query):
    print(query.data)
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
    reply_markup = createButtonMarkup(buttonList, callBackKey, str(update.effective_chat.id))
    context.bot.send_message(chat_id=targetChatId,
                             text=queryText,
                             reply_markup=reply_markup)


"""
Send emoji only 
"""


def displayButtonCard(update, context, chatid, queryText, callBackKey, cardListType):
    playerIdList, cardList = CardListType.getCardList(cardListType,chatid)
    displayCardList = []
    print("playerIdList: " + str(playerIdList))
    print("cardList: " + str(cardList))
    if cardListType == CardListType.OTHERS_PLAYER:
        """
        Display multiple decks of cards
        [cards],[cards],[cards] => [player][cards],[player][cards],[player][cards]
        """
    elif cardListType == CardListType.OWN_PLAYER or cardListType == CardListType.GRAVE:
        """
        Display single deck of cards
        """
        playCardDeck = PlayerCardDeck(cardList)
        displayCardList = [playCardDeck.topCardList]

    sendEmojiButton(context=context,
                    update=update,
                    targetChatId=chatid,
                    queryText=queryText,
                    callBackKey=callBackKey,
                    buttonList=displayCardList,
                    playerIdList=playerIdList)

def createEmojiButtonMarkup(playerIdList, buttonList, callbackKey, chatid):
    """
    :param playerNameList: list of player name
    :param buttonList:    list of card object
    :param callbackKey: text of button
    :param chatid:      channel chat id
    :return:
    """
    """
    callback_data:
    1.  callBackKey
    2.  channel id
    3.  player id
    4.  pos X
    5.  content:free to edit
    """
    keyboard = []
    for i in range(len(buttonList)):
        playName = gameData[str(chatid)]["JoinListName"][i]
        keyboard.append([InlineKeyboardButton(playName,
                                              callback_data="{},{},{},{},{}".format("Invalid", chatid, i, 0,
                                                                                    "Invalid"))])
        keyboard.append([])
        for i2 in range(len(buttonList[i])):
            keyboard[i + 1].append(InlineKeyboardButton(buttonList[i][i2].emoji,
                                                        callback_data="{},{},{},{},{}".format(callbackKey, chatid, playerIdList[i],
                                                                                              i2,
                                                                                              buttonList[i][i2].key)))
    return InlineKeyboardMarkup(keyboard)


def sendEmojiButton(context, update, targetChatId, queryText, callBackKey, buttonList, playerIdList):
    """
    :param context:      context of the chat
    :param update:       object storing chat message and channel id
    :param targetChatId: target id send to
    :param queryText:    display text on button
    :param callBackKey:  return text after click the button
    :param buttonList:   list of card object
    :return:
    """
    reply_markup = createEmojiButtonMarkup(playerIdList=playerIdList,
                                           buttonList=buttonList,
                                           callbackKey=callBackKey,
                                           chatid=update.effective_chat.id)

    context.bot.send_message(chat_id=targetChatId,
                             text=queryText,
                             reply_markup=reply_markup)


def sendMessage(context, update, targetChatId, queryText):
    return context.bot.send_message(chat_id=targetChatId,
                                    text=queryText)


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
    def wrapper(obj, update, context, chatid, posY, posX, content, fromid):
        if (fromid != gameData[str(chatid)]["JoinList"][gameData[str(chatid)]["CurrentPlayer"]]):
            return False, ""
        return fun(obj, update, context, chatid, posY, posX, content, fromid)

    return wrapper
