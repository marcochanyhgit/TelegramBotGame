class GeneralCardDeck:
    def __init__(self, cardList):
        self.cardList = cardList
        self.topCardList = self.getTopCardList()
        self.topCardEmojiList = self.getTopCardEmojiList()

    def getCardEmojiList(self):
        """
        :return: list of emoji
        """
        return [card.emoji for card in self.cardList]

    def getTopCardList(self):
        """
        :return: list of card object
        """
        print("cardlist:"+str(self.cardList))
        sortedCardList = sorted(self.cardList, key=lambda x: x.key, reverse=True)

        prevCardSkill = None
        topCardList = []
        for i in range(len(sortedCardList)):
            curCard = sortedCardList[i]
            if curCard.skill != prevCardSkill:
                topCardList.append(curCard)
            prevCardSkill = curCard.skill

        return topCardList
    def getTopCardEmojiList(self):
        return [card.emoji for card in self.topCardList]

    def remove(self,targetCardKey):
        for i in range(len(self.cardList)):
            card = self.cardList[i]
            if card.key == targetCardKey:
                self.cardList.pop(i)
                print(card.key+"removed")
                break

class PlayerCardDeck(GeneralCardDeck):
    def __init__(self, cardList):
        super(PlayerCardDeck, self).__init__(cardList)
        self.totalScores = self.getTotalScores()

    def getTotalScores(self):
        return sum([card.scores for card in self.topCardList])

