from Cards.Card import Card
import tools
from settings import CALLBACKKEY_SKILL, CardListType, gameData


class Card_Cannon(Card):
    def __init__(self, key):
        super(Card_Cannon, self).__init__(key)

    @staticmethod
    def getQueryText():
        return "Choose to Destroy One Player's Card "


    def OpenAction(self,update,context,chatid,posY,posX,content,playerName,game):
        context.bot.send_message(chat_id=chatid,text="{} has opened {}".format(playerName,self.key))
        if gameData[str(chatid)]["PlayerCards"]:
            tools.displayButtonCard(update,context,chatid,
                             queryText=self.getQueryText(),
                             callBackKey=self.skill,
                             cardListType=CardListType.OTHERS_PLAYER)
        else:
            game.ContinueTurn(update, context, chatid, posY, posX, content)

        return
