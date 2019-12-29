import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging
import random
from settings import game, gameData, CALLBACKKEY_READYSTART, CALLBACKKEY_DRAWCARD, GAMEDATA_CURRENT_GAME, \
    CALLBACKKEY_CHOOSEGAME
from DeadManDrawGame import DeadManDrawGame
from Game import Games
# class DeadManDrawGame():
#     def __init__(self, chatid, update, context):
#         # Initialize card info
#         gameData[str(chatid)]["JoinList"] = []
#         gameData[str(chatid)]["JoinListName"] = []
#         gameData[str(chatid)]["StartingGame"] = False
#         gameData[str(chatid)]["CurrentPlayer"] = 0
#         context.bot.send_message(chat_id=chatid, text="(press /join to join game)")
#         return
#
#     # ----- Game Logic ----- #
#     def GenerateCards(self):
#         deck = []
#         deck.append(Card("A1"))
#         deck.append(Card("A2"))
#         deck.append(Card("A3"))
#         deck.append(Card("A4"))
#         random.shuffle(deck)
#         return deck
#
#     def InitializeCardInfo(self, update, context, chatid, posY, posX, content):
#         # Shuffle cards, pick a starting guy #
#         gameData[str(chatid)]["CurrentPlayer"] = 0
#         gameData[str(chatid)]["Cards"] = self.GenerateCards()
#         context.bot.send_message(chat_id=chatid, text="Picked player {} as first player".format(
#             gameData[str(chatid)]["JoinListName"][gameData[str(chatid)]["CurrentPlayer"]]))
#         return
#
#     def StartTurn(self, update, context, chatid, posY, posX, content):
#         # ask to draw a card #
#         sendButton(context, update, chatid, "Player {} draw your card, or give up".format(
#             gameData[str(chatid)]["JoinListName"][gameData[str(chatid)]["CurrentPlayer"]]), CALLBACKKEY_DRAWCARD,
#                    [["Draw Card"], ["Give Up"]])
#         return
#
#     def OpenCard(self, update, context, chatid, posY, posX, content, fromid):
#         # find any thing to do after opened card #
#         print(gameData[str(chatid)]["Cards"][0])
#         context.bot.send_message(chat_id=chatid, text="Open Card")
#         return
#
#     # ---- Tools ----- #
#     def StartGame(self, update, context):
#         super().StartGame(update, context)
#         # Start a game
#         return
#
#     def showJoinList(self, update, context, chat_id):
#         listString = List2String(gameData[str(update.effective_chat.id)]["JoinListName"])
#         # context.bot.send_message(chat_id=chat_id,text="Join List: (press /join to join game)\n"+listString)
#         sendButton(context, update, chat_id, "Join List: (press /join to join game)\n" + listString,
#                    CALLBACKKEY_READYSTART, [["Ready to Start"]])
#
#     def join(self, update, context):
#         chatid = update.effective_chat.id
#         if (gameData[str(chatid)]["StartingGame"] == False):
#             if (update.message.from_user.id in gameData[str(update.effective_chat.id)]["JoinList"]):
#                 print("Exist already")
#             else:
#                 gameData[str(update.effective_chat.id)]["JoinList"].append(update.message.from_user.id)
#                 gameData[str(update.effective_chat.id)]["JoinListName"].append(update.message.from_user.first_name)
#             self.showJoinList(update, context, update.effective_chat.id)
#         else:
#             context.bot.send_message(chat_id=chatid, text="Game Started, Wait for next game")
#
#     def ReadyGame(self, update, context, chatid, posY, posX, content, fromid):
#         gameData[str(chatid)]["StartingGame"] = True
#         self.InitializeCardInfo(update, context, chatid, posY, posX, content)
#         self.StartTurn(update, context, chatid, posY, posX, content)
#         return True, "Game Start!"
#
#     def ClickedOpenedCard(self, update, context, chatid, posY, posX, content, fromid):
#         self.OpenCard(update, context, chatid, posY, posX, content)
#         return
#
#     def DrawCard(self, update, context, chatid, posY, posX, content, fromid):
#         if (fromid == gameData[str(chatid)]["JoinList"][gameData[str(chatid)]["CurrentPlayer"]]):
#             self.OpenCard(update, context, chatid, posY, posX, content, fromid)
#             return True, "Drawed card"
#         else:
#             return False, ""


# class Games():
#     NoSelected = "No Game Selected"
#     DeadManDraw = "Dead Man's Draw"
#
#
# CALLBACKKEY_CHOOSEGAME = "Choose Game"
# CALLBACKKEY_READYSTART = "Ready Start"
# CALLBACKKEY_DRAWCARD = "Draw Card"
#
# GAMEDATA_CURRENT_GAME = "Current Game"
# ----- Bot Status ----- #
# gameData = {}
# game = None


# ----- Tools ----- #
# def getButtonCallBackData(query):
#     arg = query.data.split(',')
#     return arg[0], int(arg[1]), int(arg[2]), int(arg[3]), arg[4]
#
#
# def createButtonMarkup(textList, callbackKey, chatid):
#     keyboard = []
#     for i in range(len(textList)):
#         keyboard.append([])
#         for i2 in range(len(textList[i])):
#             keyboard[i].append(InlineKeyboardButton(textList[i][i2],
#                                                     callback_data="{},{},{},{},{}".format(callbackKey, chatid, i, i2,
#                                                                                           textList[i][i2])))
#     return InlineKeyboardMarkup(keyboard)
#
#
# def sendButton(context, update, targetChatId, queryText, callBackKey, buttonList):
#     reply_markup = createButtonMarkup(buttonList, callBackKey, str(update.effective_chat.id))
#     context.bot.send_message(chat_id=targetChatId, text=queryText, reply_markup=reply_markup)
#
#
# def List2String(liststring):
#     s = ""
#     for i in liststring:
#         s = s + str(i) + "\n"
#     return s


# ----- Game Logic ----- #
from tools import getButtonCallBackData, sendButton
from settings import game,gameData

def ChooseGame(update, context, chatid, posY, posX, content, fromid):
    gameData[str(chatid)][GAMEDATA_CURRENT_GAME] = content
    StartGame(update, context, chatid, posY, posX, content)
    return True, "Chosen Game : " + content


def StartGame(update, context, chatid, posY, posX, content):
    print("Current Game is:" + gameData[str(chatid)][GAMEDATA_CURRENT_GAME])
    global game
    game = DeadManDrawGame(chatid, update, context)
    print("Success Created Game")
    return


def ReadyGame(update, context, chatid, posY, posX, content, fromid):
    print("Ready to Start Game")
    exitButtonDisplay, resultText = game.ReadyGame(update, context, chatid, posY, posX, content, fromid)
    return exitButtonDisplay, resultText


# ----- Commands ----- #

def start(update, context):
    channleChatId = update.effective_chat.id
    gameData[str(channleChatId)] = {}
    sendButton(context, update, channleChatId, "Choose Game", CALLBACKKEY_CHOOSEGAME, [[Games.DeadManDraw]])


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def join(update, context):
    game.join(update, context)


# ----- Call back handler ----- #
def button_callBack(update, context):
    query = update.callback_query
    fromid = update.callback_query.from_user.id
    callBackKey, chatid, posY, posX, content = getButtonCallBackData(query)
    print(getButtonCallBackData(query))
    if (callBackKey == CALLBACKKEY_CHOOSEGAME):
        exitButtonDisplay, resultText = ChooseGame(update, context, chatid, posY, posX, content, fromid)
    elif (callBackKey == CALLBACKKEY_READYSTART):
        exitButtonDisplay, resultText = ReadyGame(update, context, chatid, posY, posX, content, fromid)
    elif (callBackKey == CALLBACKKEY_DRAWCARD):
        exitButtonDisplay, resultText = game.DrawCard(update, context, chatid, posY, posX, content, fromid)

    if (exitButtonDisplay == True):
        query.edit_message_text(text=resultText)


# ----- Set Logging ----- #
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ----- Startup calls ----- #
botToken = "834025412:AAELXe5EvU912z50UVRIfQq9uQzhO4JtUGM"
updater = Updater(botToken, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button_callBack))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('join', join))


updater.start_polling()
updater.idle()
