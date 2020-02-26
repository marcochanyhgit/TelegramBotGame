#   Internal Import
from Cards.CardManager import CardManager
from Cards.Card_Anchor import Card_Anchor
from Cards.Card import Card
from Cards.Card_Cannon import Card_Cannon
from Cards.Card_Chest import Card_Chest
from Cards.Card_Hook import Card_Hook
from Cards.Card_Key import Card_Key
from Cards.Card_Kraken import Card_Kraken
from Cards.Card_Map import Card_Map
from Cards.Card_Mermain import Card_Mermain
from Cards.Card_Oracle import Card_Oracle
from Cards.Card_Sword import Card_Sword
from settings import game, gameData, CALLBACKKEY_READYSTART, CALLBACKKEY_DRAWCARD, CardListType, mapCount
import tools
from PlayerCardDeck import PlayerCardDeck, GeneralCardDeck
#   Built-in function
import random


class DeadManDrawGame():
    def __init__(self, chatid, update, context):
        # Initialize card info
        gameData[str(chatid)]["JoinList"] = []
        gameData[str(chatid)]["JoinListName"] = []
        gameData[str(chatid)]["StartingGame"] = False
        gameData[str(chatid)]["CurrentPlayer"] = 0
        gameData[str(chatid)]["CardsPile"] = []
        gameData[str(chatid)]["CardsOutside"] = []
        gameData[str(chatid)]["GravePile"] = []
        gameData[str(chatid)]["PlayerCards"] = []
        context.bot.send_message(chat_id=chatid, text="(press /join to join game)")
        return

    # ----- Game Logic ----- #
    def GenerateCards(self):
        deck = []

        deck.append(Card_Anchor("A2"))
        deck.append(Card_Anchor("A3"))
        deck.append(Card_Anchor("A4"))
        deck.append(Card_Anchor("A5"))
        deck.append(Card_Anchor("A6"))
        deck.append(Card_Anchor("A7"))

        # deck.append(Card_Cannon("B2"))
        # deck.append(Card_Cannon("B3"))
        # deck.append(Card_Cannon("B4"))
        # deck.append(Card_Cannon("B5"))
        # deck.append(Card_Cannon("B6"))
        # deck.append(Card_Cannon("B7"))

        deck.append(Card_Chest("C2"))
        deck.append(Card_Chest("C3"))
        deck.append(Card_Chest("C4"))
        deck.append(Card_Chest("C5"))
        deck.append(Card_Chest("C6"))
        deck.append(Card_Chest("C7"))

        # deck.append(Card_Hook("D2"))
        # deck.append(Card_Hook("D3"))
        # deck.append(Card_Hook("D4"))
        # deck.append(Card_Hook("D5"))
        # deck.append(Card_Hook("D6"))
        # deck.append(Card_Hook("D7"))

        deck.append(Card_Key("E2"))
        deck.append(Card_Key("E3"))
        deck.append(Card_Key("E4"))
        deck.append(Card_Key("E5"))
        deck.append(Card_Key("E6"))
        deck.append(Card_Key("E7"))

        deck.append(Card_Kraken("F2"))
        deck.append(Card_Kraken("F3"))
        deck.append(Card_Kraken("F4"))
        deck.append(Card_Kraken("F5"))
        deck.append(Card_Kraken("F6"))
        deck.append(Card_Kraken("F7"))

        # deck.append(Card_Map("G2"))
        # deck.append(Card_Map("G3"))
        # deck.append(Card_Map("G4"))
        # deck.append(Card_Map("G5"))
        # deck.append(Card_Map("G6"))
        # deck.append(Card_Map("G7"))

        deck.append(Card_Mermain("H4"))
        deck.append(Card_Mermain("H5"))
        deck.append(Card_Mermain("H6"))
        deck.append(Card_Mermain("H7"))
        deck.append(Card_Mermain("H8"))
        deck.append(Card_Mermain("H9"))

        # deck.append(Card_Oracle("I2"))
        # deck.append(Card_Oracle("I3"))
        # deck.append(Card_Oracle("I4"))
        # deck.append(Card_Oracle("I5"))
        # deck.append(Card_Oracle("I6"))
        # deck.append(Card_Oracle("I7"))
        #
        # deck.append(Card_Sword("J2"))
        # deck.append(Card_Sword("J3"))
        # deck.append(Card_Sword("J4"))
        # deck.append(Card_Sword("J5"))
        # deck.append(Card_Sword("J6"))
        # deck.append(Card_Sword("J7"))

        random.shuffle(deck)
        return deck

    def InitializeCardInfo(self, update, context, chatid, posY, posX, content):
        # Shuffle cards, pick a starting guy #
        gameData[str(chatid)]["CurrentPlayer"] = 0
        gameData[str(chatid)]["CardsPile"] = self.GenerateCards()
        context.bot.send_message(chat_id=chatid, text="Picked player {} as first player".format(
            gameData[str(chatid)]["JoinListName"][gameData[str(chatid)]["CurrentPlayer"]]))
        gameData[str(chatid)]["PlayerCards"] = [[] for i in range(len(gameData[str(chatid)]["JoinListName"]))]
        return

    def StartTurn(self, update, context, chatid, posY, posX, content):
        # ask to draw a card #
        gameData[str(chatid)]["CardsOutside"] = []
        tools.sendButton(context, update, chatid, "Player {} draw your card".format(
            gameData[str(chatid)]["JoinListName"][gameData[str(chatid)]["CurrentPlayer"]]), CALLBACKKEY_DRAWCARD,
                         [["Draw Card"]])
        return

    def ContinueTurn(self, update, context, chatid, posY, posX, content):
        # ask to draw a card #
        tools.sendButton(context, update, chatid, "Player {} draw your card, or give up".format(
            gameData[str(chatid)]["JoinListName"][gameData[str(chatid)]["CurrentPlayer"]]), CALLBACKKEY_DRAWCARD,
                         [["Draw Card"], ["Give Up"]])
        return

    def OpenCard(self, update, context, chatid, posY, posX, content, fromid,gotCard):
        # find any thing to do after opened card #
        print(gotCard)
        self.displayCard(update, context, chatid,
                         queryText="Previous Card: ",
                         cardList=gameData[str(chatid)]["CardsOutside"])
        self.displayCard(update, context, chatid,
                         queryText="Opened Card: ",
                         cardList=[gotCard])

        if self.CheckCardOutsideExist(gameData[str(chatid)]["CardsOutside"], gotCard):
            context.bot.send_message(chat_id=chatid, text="Busted!")
            self.CollectDeck(update, context, chatid, posY, posX, content, fromid, "Bust", gotCard)
            self.NextPlayer(update, context, chatid, posY, posX, content, fromid)
        else:
            gameData[str(chatid)]["CardsOutside"].append(gotCard)
            gotCard.OpenAction(update, context, chatid, posY, posX, content,
                               gameData[str(chatid)]["JoinListName"][gameData[str(chatid)]["CurrentPlayer"]], self)
        return

    def GiveUp(self, update, context, chatid, posY, posX, content, fromid):
        # TODO:Collect all card to deck #
        context.bot.send_message(chat_id=chatid, text="GiveUp!")
        self.CollectDeck(update, context, chatid, posY, posX, content, fromid, "GiveUp", None)
        self.NextPlayer(update, context, chatid, posY, posX, content, fromid)
        return

    def CollectDeck(self, update, context, chatid, posY, posX, content, fromid, status, gotCard):
        # collect starting deck to current player deck
        # other card throw to grave yard
        if (status == "Bust"):
            self.CollectBustDeck(chatid, gameData[str(chatid)]["CurrentPlayer"], gotCard)
        elif (status == "GiveUp"):
            self.CollectAllDeckToPlayer(chatid, gameData[str(chatid)]["CurrentPlayer"])
        print("Player:", gameData[str(chatid)]["PlayerCards"][gameData[str(chatid)]["CurrentPlayer"]])
        print("Grave:", gameData[str(chatid)]["GravePile"])
        return

    def NextPlayer(self, update, context, chatid, posY, posX, content, fromid):
        # Call next player to next turn
        gameData[str(chatid)]["CurrentPlayer"] = (gameData[str(chatid)]["CurrentPlayer"] + 1) % len(
            gameData[str(chatid)]["JoinListName"])
        self.StartTurn(update, context, chatid, posY, posX, content)
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

    @tools.localUserRequired
    def DrawCard(self, update, context, chatid, posY, posX, content, fromid):
        # if(fromid==gameData[str(chatid)]["JoinList"][gameData[str(chatid)]["CurrentPlayer"]]):
        if (content == "Draw Card"):
            gotCard = gameData[str(chatid)]["CardsPile"].pop(0)
            self.OpenCard(update, context, chatid, posY, posX, content, fromid,gotCard)
            return True, "Drawed card"
        elif (content == "Give Up"):
            self.GiveUp(update, context, chatid, posY, posX, content, fromid)
            return True, "Give Up Draw Card"
        # else:
        #     return False,""

    def CheckCardOutsideExist(self, cardList, card):
        for i in cardList:
            if (i.skill == card.skill):
                return True
        return False

    def CollectAllDeckToPlayer(self, chatid, playerId):
        while (len(gameData[str(chatid)]["CardsOutside"]) > 0):
            gameData[str(chatid)]["PlayerCards"][playerId].append(gameData[str(chatid)]["CardsOutside"].pop(0))

    def CollectBustDeck(self, chatid, playerId, gotCard):
        hasAnchor = False
        for i in gameData[str(chatid)]["CardsOutside"]:
            if (i.skill == "Anchor"):
                hasAnchor = True

        if (hasAnchor):
            gameData[str(chatid)]["GravePile"].append(gotCard)
            anchorMeet = False
            while (len(gameData[str(chatid)]["CardsOutside"]) > 0):
                card = gameData[str(chatid)]["CardsOutside"].pop(len(gameData[str(chatid)]["CardsOutside"]) - 1)
                if (anchorMeet == False):
                    gameData[str(chatid)]["GravePile"].append(card)
                else:
                    gameData[str(chatid)]["PlayerCards"][playerId].append(card)

                if (card.skill == "Anchor"):
                    anchorMeet = True

        else:
            gameData[str(chatid)]["GravePile"].append(gotCard)
            while (len(gameData[str(chatid)]["CardsOutside"]) > 0):
                card = gameData[str(chatid)]["CardsOutside"].pop(0)
                gameData[str(chatid)]["GravePile"].append(card)


    @staticmethod
    def displayCard(update, context, targetChatId, queryText, cardList, callBackKey=None, isUniqueTop=False):
        """
        :param isUniqueTop: True for showing the top of the cards [A5,A4,A7,B4,B5] -> [A7,B5]
        :return:
        """
        if isUniqueTop:
            playCardDeck = PlayerCardDeck(cardList)
            displayCardList = [playCardDeck.topCardList]

            tools.sendEmojiButton(context=context,
                                  update=update,
                                  targetChatId=targetChatId,
                                  queryText=queryText,
                                  callBackKey=callBackKey,
                                  buttonList=displayCardList)
        else:
            """
            display player playing card
            query text = Opened Card    cardList = [<Card_A4>,<Card_A5>,...] 
            =>
            Opened Card: Emoji , Emoji , Emoji
            """

            cardKeyList = PlayerCardDeck(cardList).getCardEmojiList()
            queryText += "" + " , ".join(cardKeyList)

            tools.sendMessage(context=context,
                              update=update,
                              targetChatId=targetChatId,
                              queryText=queryText)


class SkillManager:
    @staticmethod
    def DoAction( update,context,chatid,posY,posX,fromid,callBackKey,selectedPlayerId,selectedCardKey,content):
        print(gameData[str(chatid)]["PlayerCards"])
        targetPlayerCardDeck = PlayerCardDeck(gameData[str(chatid)]["PlayerCards"][selectedPlayerId])
        _,currentPlayerDeck = CardListType.getCardList(CardListType.OWN_PLAYER,chatid)
        currentPlayerCardDeck = PlayerCardDeck(currentPlayerDeck)
        cardDeck = CardListType.getCardList(CardListType.DECK,chatid)
        graveDeck = CardListType.getCardList(CardListType.GRAVE, chatid)

        if callBackKey == "Cannon":
            #put player's card to grave
            grabCard = targetPlayerCardDeck.remove(selectedCardKey)
            graveDeck.append(grabCard)
            print(graveDeck)
            print(targetPlayerCardDeck)
            resultMessage = "You destroyed player {} {}.".format(gameData[str(chatid)]["JoinListName"][0],selectedCardKey)
            return True , resultMessage
        elif callBackKey == "Hook":
            grabCard = currentPlayerCardDeck.remove(selectedCardKey)
            game.OpenCard(update,context,chatid,posY,posX,
                                     content=callBackKey,
                                     fromid=fromid,
                                     gotCard=grabCard)
            #play selected card
        elif callBackKey == "Map":
            graveCardDeck = GeneralCardDeck(graveDeck)
            grabCard = graveCardDeck.remove(selectedCardKey)
            mapCount.append(grabCard)
            currentPlayerDeck.append(grabCard)
            resultMessage = "You get card {} from grave.".format(selectedCardKey)
            if len(mapCount) == 3 or not graveCardDeck:
                mapCount.clear()
                return True, resultMessage
            else:
                gameData[str(chatid)]["CardsOutside"][-1].OpenAction(update,context,chatid,posY,posX,content,
                    gameData[str(chatid)]["JoinListName"][gameData[str(chatid)]["CurrentPlayer"]],game)
            #play selected card
        elif callBackKey == "Sword":
             grabCard = targetPlayerCardDeck.remove(selectedCardKey)
             game.OpenCard(update,context,chatid,posY,posX,
                                      content=callBackKey,
                                      fromid=fromid,
                                      gotCard=grabCard)
        elif callBackKey == "Oracle":
            pass
