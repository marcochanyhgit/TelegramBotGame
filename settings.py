global gameData
global game
gameData = {}
game = None

CALLBACKKEY_CHOOSEGAME = "Choose Game"
CALLBACKKEY_READYSTART = "Ready Start"
CALLBACKKEY_DRAWCARD = "Draw Card"
CALLBACKKEY_SKILL = "Skill"

GAMEDATA_CURRENT_GAME = "Current Game"


class CardListType:
    OTHERS_PLAYER = "Others"
    OWN_PLAYER = "Own"
    GRAVE = "Grave"
    DECK = "Deck"
    @staticmethod
    def getCardList(cardListType,chatid):
        chatDict = gameData[str(chatid)]
        if cardListType == CardListType.OTHERS_PLAYER:
            othersPlayerCards = []
            playerIdList = []
            for playerid in range(len(chatDict["JoinList"])):
                if (chatDict["CurrentPlayer"] != playerid):
                    othersPlayerCards.append(chatDict["PlayerCards"][playerid])
                    playerIdList.append(chatDict["JoinList"][playerid])
            return playerIdList , othersPlayerCards
        elif cardListType == CardListType.OWN_PLAYER:
            return [chatDict["JoinList"][chatDict["CurrentPlayer"]]],chatDict["PlayerCards"][chatDict["CurrentPlayer"]]
        elif cardListType == CardListType.GRAVE:
            return chatDict["GravePile"]
        elif cardListType == CardListType.DECK:
            return chatDict["CardsPile"]



