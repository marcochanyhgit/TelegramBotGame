#   Internal Import
from Card import Card
from settings import game, gameData, CALLBACKKEY_READYSTART, CALLBACKKEY_DRAWCARD
import tools
#   Built-in function
import random

class DeadManDrawGame():
    def __init__(self, chatid, update, context):
        # Initialize card info
        gameData[str(chatid)]["JoinList"]=[]
        gameData[str(chatid)]["JoinListName"]=[]
        gameData[str(chatid)]["StartingGame"]=False
        gameData[str(chatid)]["CurrentPlayer"]=0
        gameData[str(chatid)]["CardsPile"]=[]
        gameData[str(chatid)]["CardsOutside"]=[]
        gameData[str(chatid)]["GravePile"]=[]
        context.bot.send_message(chat_id=chatid, text="(press /join to join game)")
        return

    # ----- Game Logic ----- #
    def GenerateCards(self):
        deck = []

        deck.append(Card("A2"))
        deck.append(Card("A3"))
        deck.append(Card("A4"))
        deck.append(Card("A5"))
        deck.append(Card("A6"))
        deck.append(Card("A7"))

        deck.append(Card("B2"))
        deck.append(Card("B3"))
        deck.append(Card("B4"))
        deck.append(Card("B5"))
        deck.append(Card("B6"))
        deck.append(Card("B7"))
        
        deck.append(Card("C2"))
        deck.append(Card("C3"))
        deck.append(Card("C4"))
        deck.append(Card("C5"))
        deck.append(Card("C6"))
        deck.append(Card("C7"))
        
        deck.append(Card("D2"))
        deck.append(Card("D3"))
        deck.append(Card("D4"))
        deck.append(Card("D5"))
        deck.append(Card("D6"))
        deck.append(Card("D7"))
        
        deck.append(Card("E2"))
        deck.append(Card("E3"))
        deck.append(Card("E4"))
        deck.append(Card("E5"))
        deck.append(Card("E6"))
        deck.append(Card("E7"))
        
        deck.append(Card("F2"))
        deck.append(Card("F3"))
        deck.append(Card("F4"))
        deck.append(Card("F5"))
        deck.append(Card("F6"))
        deck.append(Card("F7"))
        
        deck.append(Card("G2"))
        deck.append(Card("G3"))
        deck.append(Card("G4"))
        deck.append(Card("G5"))
        deck.append(Card("G6"))
        deck.append(Card("G7"))
        
        deck.append(Card("H4"))
        deck.append(Card("H5"))
        deck.append(Card("H6"))
        deck.append(Card("H7"))
        deck.append(Card("H8"))
        deck.append(Card("H9"))
        
        deck.append(Card("I2"))
        deck.append(Card("I3"))
        deck.append(Card("I4"))
        deck.append(Card("I5"))
        deck.append(Card("I6"))
        deck.append(Card("I7"))
        
        deck.append(Card("J2"))
        deck.append(Card("J3"))
        deck.append(Card("J4"))
        deck.append(Card("J5"))
        deck.append(Card("J6"))
        deck.append(Card("J7"))

        random.shuffle(deck)
        return deck

    def InitializeCardInfo(self, update, context, chatid, posY, posX, content):
        # Shuffle cards, pick a starting guy #
        gameData[str(chatid)]["CurrentPlayer"] = 0
        gameData[str(chatid)]["CardsPile"] = self.GenerateCards()
        context.bot.send_message(chat_id=chatid,text="Picked player {} as first player".format(
            gameData[str(chatid)]["JoinListName"][gameData[str(chatid)]["CurrentPlayer"]]))
        return

    def StartTurn(self, update, context, chatid, posY, posX, content):
        # ask to draw a card #
        gameData[str(chatid)]["CardsOutside"]=[]
        tools.sendButton(context,update,chatid,"Player {} draw your card".format(
            gameData[str(chatid)]["JoinListName"][gameData[str(chatid)]["CurrentPlayer"]]),CALLBACKKEY_DRAWCARD,
            [["Draw Card"]])
        return

    def ContinueTurn(self,update,context,chatid,posY,posX,content):
        # ask to draw a card #
        tools.sendButton(context,update,chatid,"Player {} draw your card, or give up".format(gameData[str(chatid)]["JoinListName"][gameData[str(chatid)]["CurrentPlayer"]]),CALLBACKKEY_DRAWCARD,[["Draw Card"],["Give Up"]])
        return

    def OpenCard(self, update, context, chatid, posY, posX, content, fromid):
        # find any thing to do after opened card #
        context.bot.send_message(chat_id=chatid,text="Opened Card"+gameData[str(chatid)]["CardsPile"][0].key)
        gotCard=gameData[str(chatid)]["CardsPile"].pop(0)
        if(self.CheckCardOutsideExist(gameData[str(chatid)]["CardsOutside"],gotCard)):
            context.bot.send_message(chat_id=chatid,text="Busted!")
            self.CollectDeck(update, context, chatid, posY, posX, content, fromid, "Bust")
            self.NextPlayer(update,context,chatid,posY,posX,content,fromid)
        else:
            gameData[str(chatid)]["CardsOutside"].append(gotCard)
            gotCard.OpenAction(update,context,chatid,posY,posX,content,gameData[str(chatid)]["JoinListName"][gameData[str(chatid)]["CurrentPlayer"]],self)
        return

    def GiveUp(self,update,context,chatid,posY,posX,content,fromid):
        # TODO:Collect all card to deck #
        context.bot.send_message(chat_id=chatid,text="GiveUp!")
        self.CollectDeck(update, context, chatid, posY, posX, content, fromid, "GiveUp")
        self.NextPlayer(update,context,chatid,posY,posX,content,fromid)
        return

    def CollectDeck(self,update,context,chatid,posY,posX,content,fromid,status):
        #collect starting deck to current player deck
        #other card throw to grave yard
        return

    def NextPlayer(self,update,context,chatid,posY,posX,content,fromid):
        # Call next player to next turn
        gameData[str(chatid)]["CurrentPlayer"] = (gameData[str(chatid)]["CurrentPlayer"] +1)%len(gameData[str(chatid)]["JoinListName"])
        self.StartTurn(update,context,chatid,posY,posX,content)
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
        if(fromid==gameData[str(chatid)]["JoinList"][gameData[str(chatid)]["CurrentPlayer"]]):
            if(content=="Draw Card"):
                self.OpenCard(update,context,chatid,posY,posX,content,fromid)
                return True,"Drawed card"
            elif(content=="Give Up"):
                self.GiveUp(update,context,chatid,posY,posX,content,fromid)
                return True,"Give Up Draw Card"
        else:
            return False,"" 

    def CheckCardOutsideExist(self,cardList,card):
        for i in cardList:
            if(i.skill==card.skill):
                return True
        return False