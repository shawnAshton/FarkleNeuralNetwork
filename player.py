import random


class Player:
    def __init__(self):
        self.totalScore = 0
        self.roundScore = 0

    def freeze(self, frozen):
        """
        randomly freezes valid dice, so that they will not be rolled again
        """
        freeze_dice = []
        for i in range(6):
            if frozen[i] is 1:
                freeze_dice.append(random.randint(0, 1))
            else:
                freeze_dice.append(0)
        return freeze_dice
