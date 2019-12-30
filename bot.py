import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging
import random
from settings import game, gameData, CALLBACKKEY_READYSTART, CALLBACKKEY_DRAWCARD, GAMEDATA_CURRENT_GAME, \
    CALLBACKKEY_CHOOSEGAME
from DeadManDrawGame import DeadManDrawGame
from Game import Games

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
botToken = "1043079672:AAGKrVHxXkROQTZG-T9CQ0gyjGw4hzEls5s"
updater = Updater(botToken, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button_callBack))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('join', join))


updater.start_polling()
updater.idle()
