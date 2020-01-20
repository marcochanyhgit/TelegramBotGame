from .Card import Card

class Card_Key(Card):
    def OpenAction(self,update,context,chatid,posY,posX,content,playerName,game):
        context.bot.send_message(chat_id=chatid,text="{} has opened {}".format(playerName,self.key))
        game.ContinueTurn(update,context,chatid,posY,posX,content)
        return