#   Internal Import
from Card import Card
from settings import game, gameData, CALLBACKKEY_READYSTART, CALLBACKKEY_DRAWCARD
import tools
#   Built-in function
import random

class DeadManDrawGame():
    def __init__(self, chatid, update, context):
        # Initialize card info
        gameData[str(chatid)]["JoinList"] = []
        gameData[str(chatid)]["JoinListName"] = []
        gameData[str(chatid)]["StartingGame"] = False
        gameData[str(chatid)]["CurrentPlayer"] = 0
        context.bot.send_message(chat_id=chatid, text="(press /join to join game)")
        return

    # ----- Game Logic ----- #
    def GenerateCards(self):
        deck = []
        deck.append(Card("A1"))
        deck.append(Card("A2"))
        deck.append(Card("A3"))
        deck.append(Card("A4"))
        random.shuffle(deck)
        return deck

    def InitializeCardInfo(self, update, context, chatid, posY, posX, content):
        # Shuffle cards, pick a starting guy #
        gameData[str(chatid)]["CurrentPlayer"] = 0
        gameData[str(chatid)]["Cards"] = self.GenerateCards()
        context.bot.send_message(chat_id=chatid, text="Picked player {} as first player".format(
            gameData[str(chatid)]["JoinListName"][gameData[str(chatid)]["CurrentPlayer"]]))
        return

    def StartTurn(self, update, context, chatid, posY, posX, content):
        # ask to draw a card #
        tools.sendButton(context, update, chatid, "Player {} draw your card, or give up".format(
            gameData[str(chatid)]["JoinListName"][gameData[str(chatid)]["CurrentPlayer"]]), CALLBACKKEY_DRAWCARD,
                   [["Draw Card"], ["Give Up"]])
        return

    def OpenCard(self, update, context, chatid, posY, posX, content, fromid):
        # find any thing to do after opened card #
        print(gameData[str(chatid)]["Cards"][0])
        context.bot.send_message(chat_id=chatid, text="Open Card")
        return

    # ---- Tools ----- #
    def StartGame(self, update, context):
        super().StartGame(update, context)
        # Start a game
        return

    def showJoinList(self, update, context, chat_id):
        listString = tools.List2String(gameData[str(update.effective_chat.id)]["JoinListName"])
        # context.bot.send_message(chat_id=chat_id,text="Join List: (press /join to join game)\n"+listString)
        tools.sendButton(context, update, chat_id, "Join List: (press /join to join game)\n" + listString,
                   CALLBACKKEY_READYSTART, [["Ready to Start"]])

    def join(self, update, context):
        chatid = update.effective_chat.id
        if (gameData[str(chatid)]["StartingGame"] == False):
            if (update.message.from_user.id in gameData[str(update.effective_chat.id)]["JoinList"]):
                print("Exist already")
            else:
                gameData[str(update.effective_chat.id)]["JoinList"].append(update.message.from_user.id)
                gameData[str(update.effective_chat.id)]["JoinListName"].append(update.message.from_user.first_name)
            self.showJoinList(update, context, update.effective_chat.id)
        else:
            context.bot.send_message(chat_id=chatid, text="Game Started, Wait for next game")

    def ReadyGame(self, update, context, chatid, posY, posX, content, fromid):
        gameData[str(chatid)]["StartingGame"] = True
        self.InitializeCardInfo(update, context, chatid, posY, posX, content)
        self.StartTurn(update, context, chatid, posY, posX, content)
        return True, "Game Start!"

    def ClickedOpenedCard(self, update, context, chatid, posY, posX, content, fromid):
        self.OpenCard(update, context, chatid, posY, posX, content)
        return

    def DrawCard(self, update, context, chatid, posY, posX, content, fromid):
        if (fromid == gameData[str(chatid)]["JoinList"][gameData[str(chatid)]["CurrentPlayer"]]):
            self.OpenCard(update, context, chatid, posY, posX, content, fromid)
            return True, "Drawed card"
        else:
            return False, ""

