from Cards.Card import Card
from Cards.Card_Anchor import Card_Anchor
from Cards.Card_Cannon import Card_Cannon
from Cards.Card_Hook import Card_Hook
from Cards.Card_Map import Card_Map
from Cards.Card_Oracle import Card_Oracle
from Cards.Card_Sword import Card_Sword


class CardManager(Card):
    @staticmethod
    def creation(key):
        if "A" in key:
            return Card_Anchor(key)
        elif "B" in key:
            return Card_Cannon(key)
        # elif "C" in key:
        #     return Card_Chest(key)
        elif "D" in key:
            return Card_Hook(key)
        # elif "E" in key:
        #     return Card_Key(key)
        # elif "F" in key:
        #     return Card_Kraken(key)
        # elif "G" in key:
        #     return Card_Map(key)
        # elif "H" in key:
        #     return Card_Mermain(key)
        elif "I" in key:
            return Card_Oracle(key)
        elif "J" in key:
            return Card_Sword(key)
