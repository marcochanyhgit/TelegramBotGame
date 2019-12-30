from .Card import Card

class Card_Anchor(Card):

    def OpenAction(self,update,context,chatid,posY,posX,content,playerName,game):
        print("Called Anchor")
        context.bot.send_message(chat_id=chatid,text="{} has opened {}".format(playerName,self.key))
        game.ContinueTurn(update,context,chatid,posY,posX,content)
        return