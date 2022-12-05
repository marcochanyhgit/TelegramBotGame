global gameData
global game
global mapCount
gameData = {}
game = None
mapCount = []

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
    All ="All"
    @staticmethod
    def getCardList(cardListType,chatid):
        chatDict = gameData[str(chatid)]
        if cardListType == CardListType.OTHERS_PLAYER:
            othersPlayerCards = []
            playerIdList = []
            for playerid in range(len(chatDict["JoinList"])):
                # if (playerid != chatDict["CurrentPlayer"]):
                othersPlayerCards.append(chatDict["PlayerCards"][playerid])
                playerIdList.append(playerid)
            return playerIdList , chatDict["PlayerCards"]
        elif cardListType == CardListType.OWN_PLAYER:
            return [chatDict["JoinList"][chatDict["CurrentPlayer"]]],chatDict["PlayerCards"][chatDict["CurrentPlayer"]]
        elif cardListType == CardListType.GRAVE:
            return chatDict["GravePile"]
        elif cardListType == CardListType.DECK:
            return chatDict["CardsPile"]
        elif cardListType == CardListType.All:
            return chatDict["PlayerCards"]



