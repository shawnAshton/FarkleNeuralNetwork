import random
from collections import Counter


class Game:
    def __init__(self):
        self.dice = []
        # Start of a game, so everything is valid
        self.reRoll = [1, 1, 1, 1, 1, 1]  # frozen... 1 means we can roll that dice

    def randomize_dice(self):
        """
        Randomize a list of six dice.
        Ignore those dice that are marked as frozen
        "Frozen" dice are simply marked as zeros.
        """
        temp_dice = self.dice

        self.dice = []
        for i in range(6):
            if self.reRoll[i] is 1:
                self.dice.append(random.randint(1, 6))
            else:
                self.dice.append(temp_dice[i])

    def randomize_fake_dice(self, dice, reRoll):
        """
        Randomize a list of six dice.
        Ignore those dice that are marked as frozen
        "Frozen" dice are simply marked as zeros.
        """
        temp_dice = dice

        dice = []
        for i in range(6):
            if reRoll[i] is 1:
                dice.append(random.randint(1, 6))
            else:
                dice.append(temp_dice[i])
        return dice

    def score_roll(self, dice, reRoll):
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
        dice_to_keep = []
        for i in range(len(dice)):
            # print('dice at index i is:', i, self.dice[i])
            if reRoll[i] == 0:
                dice_to_keep.append(dice[i])
        count = Counter(dice_to_keep)
        score = 0
        # print('THIS IS THE LENGHT', len(dice_to_keep))
        if len(dice_to_keep) > 0:
            if count[1] >= 3:
                # print('A')
                score += 1000
                score += (count[1] - 3) * 100
                score += count[5] * 50
            elif count[5] >= 3:
                # print('B')
                score += 500
                score += (count[5] - 3) * 50
                score += count[1] * 100
            elif count.most_common(1)[0][1] >= 3:
                # print('C')
                score += count.most_common(1)[0][0] * 100
                score += count[1] * 100
                score += count[5] * 50
            else:
                # print('D')
                score += count[5] * 50
                score += count[1] * 100
        # print('MY SCORE IS NOW', score)
        # print('MY DICE', dice_to_keep)
        return score

    def is_valid_move(self, frozen):
        """
        This determines if removing a certain die is valid or not
        Frozen must be a list of size six. It must consist of only 0 or 1
        :param frozen:
        :return:
        """

        count_of_player_frozen = Counter(frozen)
        count_of_game_frozen = Counter(self.reRoll)

        # Special case: Restarting round
        if not any(frozen):
            self.reRoll = [1, 1, 1, 1, 1, 1]
            return True

        # obvious false....
        if count_of_player_frozen[0] <= count_of_game_frozen[0]:
            return False
        else:
            # now we see if it freezes the same stuff as last time... if it doesn't it is an error
            just_frozen = []
            for i, gameFrozen in enumerate(self.reRoll):
                if gameFrozen == 0:
                    #  if gameFrozen is zero.... below BETTER be frozen
                    if frozen[i] != 0:
                        return False
                elif gameFrozen == 1 and frozen[i] == 0:
                    just_frozen.append(self.dice[i])

            all_frozen = []
            for i, die in enumerate(frozen):
                if die is 0:
                    all_frozen.append(self.dice[i])

            triples = Counter(all_frozen)

            # did the player decide to freeze some points? points that were additional to what was already frozen?
            for i, gameFrozen in enumerate(self.reRoll):
                # if game frozen is not 0... worry about the index......
                if gameFrozen != 0:
                    # this was just FROZEN is it a scoring dice??
                    if frozen[i] == 0:
                        if self.dice[i] == 1 or self.dice[i] == 5:
                            self.reRoll = frozen
                            return True

            # Check to see if we have a triple
            for die in just_frozen:
                if triples[die] >= 3:
                    self.reRoll = frozen
                    return True

            # What do we do here? Do we force rules?
            return False
