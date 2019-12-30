class PlayerCardDeck:
    def __init__(self, cardList):
        self.cardList = cardList
        self.topCardList = self.getTopCardList()
        self.totalScores = self.getTotalScores()

    def getTopCardList(self):
        sortedCardList = sorted(self.cardList, key=lambda x: x.key, reverse=True)

        prevCardSkill = None
        topCardList = []
        for i in range(len(sortedCardList)):
            curCard = sortedCardList[i]
            if curCard.skill != prevCardSkill:
                topCardList.append(curCard)
            prevCardSkill = curCard.skill

        return topCardList

    def getTotalScores(self):
        return sum([card.scores for card in self.topCardList])

