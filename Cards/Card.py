
"""
    Card skills

    Key - Name - skills

    A - Anchor – Keep everything you drew before the Anchor even if you bust.

    B - Cannon – Destroy one card an opponent has previously banked.

    C - Chest – Double your haul by banking as many cards directly from the discard pile as are in the river when you bank the Chest – but only if you also bank a Key.

    D - Hook – Play one of your previously banked cards.

    E - Key – Enables the Chest special.

    F - Kraken – Oh no! You’re forced to draw at least two more cards.

    G - Map – Draw three cards from the discard pile and play one.

    H - Mermaid – No ability, but worth more points (Mermaids are numbered 4-9 instead of 2-7).

    I - Oracle – Look at the next card before deciding if you want to play it.

    J - Sword – Steal an opponent’s previously banked card and play it.
"""


Skills = {
    "A": "Anchor",
    "B": "Cannon",
    "C": "Chest",
    "D": "Hook",
    "E": "Key",
    "F": "Kraken",
    "G": "Map",
    "H": "Mermaid",
    "I": "Oracle",
    "J": "Sword"
}

Emoji = {
    "Anchor":'⚓',
    "Cannon":'💣',
    "Chest":'💰',
    "Hook":'✔',
    "Key":'🔑',
    "Kraken":'🐙',
    "Map":'📜',
    "Mermaid":'🐟',
     "Oracle":'🔮',
    "Sword":'🗡',
    1:"1⃣",        
    2:"2⃣",
    3:"3⃣",
    4:"4⃣",
    5:"5⃣",
    6:"6⃣",
    7:"7⃣",
    8:"8⃣",
    9:"9⃣"
}


class Card():
    def __init__(self, key):
        self.key = key
        self.skill, self.scores = self.getCardFields()
        self.emoji = self.display()

    def __str__(self):
        return "Card_"+str(self.key)

    def display(self):
        return Emoji[self.skill]+Emoji[self.scores]

    def getCardFields(self):
        """
        example key : A4 means skill Anchor with score 4
        :return:
        """
        skill = Skills[self.key[0]]
        scores = int(self.key[1])
        return skill, scores

    def OpenAction(self,update,context,chatid,posY,posX,content,playerName,game):
        context.bot.send_message(chat_id=chatid,text="{} has opened {}".format(playerName,self.key))
        game.ContinueTurn(update,context,chatid,posY,posX,content)
        return
