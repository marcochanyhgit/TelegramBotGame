import tools
from Cards.Card import Card
from settings import CardListType


class Card_Map(Card):
    def __init__(self, key):
        super(Card_Map, self).__init__(key)

    @staticmethod
    def getQueryText():
        return "Choose one Card to your Deck"

    def OpenAction(self,update,context,chatid,posY,posX,content,playerName,game):
        context.bot.send_message(chat_id=chatid,text="{} has opened {}".format(playerName,self.key))

        tools.displayButtonCard(update, context, chatid,
                                queryText=self.getQueryText(),
                                callBackKey=self.skill,
                                cardListType=CardListType.GRAVE)

        game.ContinueTurn(update,context,chatid,posY,posX,content)
        return