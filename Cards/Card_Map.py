from Cards.Card import Card

class Card_Map(Card):
    def __init__(self, key):
        super(Card_Map, self).__init__(key)

    def OpenAction(self,update,context,chatid,posY,posX,content,playerName,game):
        context.bot.send_message(chat_id=chatid,text="{} has opened {}".format(playerName,self.key))
        game.ContinueTurn(update,context,chatid,posY,posX,content)
        return