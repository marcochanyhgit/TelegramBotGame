from Cards.Card import Card
# from Cards import cardNumber



class Card_Hook(Card):
    def __init__(self, key):
        super(Card_Hook, self).__init__(key)

    def OpenAction(self,update,context,chatid,posY,posX,content,playerName,game):
        context.bot.send_message(chat_id=chatid,text="{} has opened {}".format(playerName,self.key))
        game.ContinueTurn(update,context,chatid,posY,posX,content)
        return