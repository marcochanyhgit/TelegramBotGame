from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging



class DeadManDrawGame():
    def __init__(self,chatid,update,context):
        # Initialize card info
        gameData[str(chatid)]["JoinList"]=[]
        gameData[str(chatid)]["JoinListName"]=[]
        gameData[str(chatid)]["StartingGame"]=False
        context.bot.send_message(chat_id=chatid,text="(press /join to join game)")
        return

    # ----- Game Logic ----- #

    def InitializeCardInfo(self,update,context,chatid,posY,posX,content):
        # Start cards, pick a starting guy #
        context.bot.send_message(chat_id=chatid,text="Picked player X as first player")
        return

    def StartTurn(self,update,context,chatid,posY,posX,content):
        # ask to draw a card #
        context.bot.send_message(chat_id=chatid,text="Player X draw your card, or give up")
        return
    
    def OpenCard(self,update,context,chatid,posY,posX,content):
        # find any thing to do after opened card #
        context.bot.send_message(chat_id=chatid,text="Open Card")
        return
    

    # ---- Tools ----- #
    def StartGame(self,update,context):
        super().StartGame(update,context)
        # Start a game
        return
        
    def showJoinList(self,update,context,chat_id):
        listString=List2String(gameData[str(update.effective_chat.id)]["JoinListName"])
        # context.bot.send_message(chat_id=chat_id,text="Join List: (press /join to join game)\n"+listString)
        sendButton(context,update,chat_id,"Join List: (press /join to join game)\n"+listString,CALLBACKKEY_READYSTART,[["Ready to Start"]])

    def join(self,update,context):
        chatid=update.effective_chat.id
        if(gameData[str(chatid)]["StartingGame"]==False):
            if(update.message.from_user.id in gameData[str(update.effective_chat.id)]["JoinList"]):
                print("Exist already")
            else:
                gameData[str(update.effective_chat.id)]["JoinList"].append(update.message.from_user.id)
                gameData[str(update.effective_chat.id)]["JoinListName"].append(update.message.from_user.first_name)
            self.showJoinList(update,context,update.effective_chat.id)
        else:
            context.bot.send_message(chat_id=chatid,text="Game Started, Wait for next game")

    def ReadyGame(self,update,context,chatid,posY,posX,content):
        context.bot.send_message(chat_id=chatid,text="Game Started")
        gameData[str(chatid)]["StartingGame"]=True
        self.InitializeCardInfo(update,context,chatid,posY,posX,content)
        self.StartTurn(update,context,chatid,posY,posX,content)

    def ClickedOpenedCard(self,update,context,chatid,posY,posX,content):
        self.OpenCard(update,context,chatid,posY,posX,content)
        return
    
    
    
    

class Games():
    NoSelected="No Game Selected"
    DeadManDraw="Dead Man's Draw"


CALLBACKKEY_CHOOSEGAME="Choose Game"
CALLBACKKEY_READYSTART="Ready Start"

GAMEDATA_CURRENT_GAME="Current Game"
# ----- Bot Status ----- #
gameData={}
game=None

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

def List2String(liststring):
    s=""
    for i in liststring:
        s=s+str(i)+"\n"
    return s


# ----- Game Logic ----- #

def ChooseGame(update,context,chatid,posY,posX,content):
    context.bot.send_message(chat_id=chatid, text='Choosen Game : {}'.format(content))
    gameData[str(chatid)][GAMEDATA_CURRENT_GAME]=content
    StartGame(update,context,chatid,posY,posX,content)
    return

def StartGame(update,context,chatid,posY,posX,content):
    print("Current Game is:"+gameData[str(chatid)][GAMEDATA_CURRENT_GAME])
    global game
    game=DeadManDrawGame(chatid,update,context)
    print("Success Created Game")
    return

def ReadyGame(update,context,chatid,posY,posX,content):
    print("Ready to Start Game")
    game.ReadyGame(update,context,chatid,posY,posX,content)
    return
# ----- Commands ----- #

def start(update, context):
    gameData[str(update.effective_chat.id)]={}
    sendButton(context,update,update.effective_chat.id,"Choose Game",CALLBACKKEY_CHOOSEGAME,[[Games.DeadManDraw]])


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")

def join(update,context):
    game.join(update,context)

# ----- Call back handler ----- #
def button_callBack(update, context):
    query = update.callback_query
    callBackKey,chatid,posY,posX,content=getButtonCallBackData(query)
    query.edit_message_text(text="Selected : {}".format(content))
    if(callBackKey==CALLBACKKEY_CHOOSEGAME):
        ChooseGame(update,context,chatid,posY,posX,content)
    elif(callBackKey==CALLBACKKEY_READYSTART):
        ReadyGame(update,context,chatid,posY,posX,content)


# ----- Startup calls ----- #
updater = Updater('1043079672:AAGKrVHxXkROQTZG-T9CQ0gyjGw4hzEls5s', use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button_callBack))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('join', join))
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)
updater.start_polling()
updater.idle()
