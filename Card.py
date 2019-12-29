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

Stickers = {

}

class Card():
    def __init__(self, key):
        self.key = key
        self.skill, self.scores = self.getCardFields()
    def getCardFields(self):
        """
        example key : A4 means skill Anchor with score 4
        :return:
        """
        skill = Skills[self.key[0]]
        scores = int(self.key[1])
        return skill,scores
    def OpenAction(self):
        return

