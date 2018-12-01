import random
from collections import Counter


class Game:
    def __init__(self):
        self.dice = []
        # Start of a game, so everything is valid
        self.frozen = [1, 1, 1, 1, 1, 1]  # frozen... 1 means we can roll that dice

    def randomize_dice(self):
        """
        Randomize a list of six dice.
        Ignore those dice that are marked as frozen
        "Frozen" dice are simply marked as zeros.
        """
        self.dice = []

        for i in range(6):
            if self.frozen[i] is 1:
                self.dice.append(random.randint(1, 6))
            else:
                self.dice.append(0)

    def score_roll(self):
        """
        Scores the dice.
        1 = 100
        5 = 50
        Triples = tripleDie * 100 (Ex. 4,4,4 = 400)
        Triple 1 = 1000
        Everything else = 0
        :return:
        The score of the dice roll
        """
        count = Counter(self.dice)
        score = 0
        if count[1] >= 3:
            score += 1000
            score += (count[1] - 3) * 100
            score += count[5] * 50
        elif count[5] >= 3:
            score += 500
            score += (count[5] - 3) * 50
            score += count[1] * 100
        elif count.most_common(1)[0][1] >= 3:
            score += count.most_common(1)[0][0] * 100
            score += count[1] * 100
            score += count[5] * 50
        else:
            score += count[5] * 50
            score += count[1] * 100
        return score

    def is_valid_move(self, frozen):
        """
        This determines if removing a certain die is valid or not
        Frozen must be a list of size six. It must consist of only 0 or 1
        :param frozen:
        :return:
        """
        count_of_frozen = Counter(frozen)
        count_of_already_frozen = Counter(self.frozen)

        if count_of_frozen[0] == 6:
            # Everything is frozen, so start a new round
            self.frozen = [1, 1, 1, 1, 1, 1]
            return True
        elif count_of_frozen[0] > count_of_already_frozen[0]:
            # Is there a triple? What number is it?
            count = Counter(self.dice)
            die = 0
            if count.most_common(1)[0][1] >= 3:
                die = count.most_common(1)[0][0]

            counter = 0
            # Is this a valid move?
            valid = False
            # We might have a valid turn, double check that points are being frozen
            for i in range(len(frozen)):
                # Freeze the selected ones or fives from being played
                if (self.dice[i] is 1 or self.dice[i] is 5) and frozen[i] is 0:
                    self.frozen[i] = 0
                    valid = True
                # Freeze triples from being played
                if die is not 0 and self.dice[i] is die and counter < 3:
                    counter += 1
                    self.frozen[i] = 0
                    valid = True
            return valid
        else:
            # The only two valid scenarios are above, so this is false
            return False
