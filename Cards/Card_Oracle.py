from Cards.Card import Card
from settings import CardListType


class Card_Oracle(Card):
    def __init__(self, key):
        super(Card_Oracle, self).__init__(key)

    def OpenAction(self,update,context,chatid,posY,posX,content,playerName,game):
        context.bot.send_message(chat_id=chatid,text="{} has opened {}".format(playerName,self.key))
        fromid = update.callback_query.from_user.id
        cardDeck = CardListType.getCardList(CardListType.DECK, chatid)
        if cardDeck:
            grabCard = cardDeck.pop(0)
            context.bot.send_message(chat_id=fromid, text="The card on top is {}".format(grabCard.emoji))

        game.ContinueTurn(update,context,chatid,posY,posX,content)
        return

