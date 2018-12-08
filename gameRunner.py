import rules
import greedy_player
import tensorflow as tf

class GameRunner:
    def __init__(self, player, farkle, tensor_session, learning_rate_decay, learning_rate_start, learning_rate_min):
        self.player = player
        self.farkle = farkle
        self.tensor_session = tensor_session
        self.learning_rate_decay = learning_rate_decay
        self.learning_rate_start = learning_rate_start
        self.learning_rate_min = learning_rate_min

    def run(self):
        average = 0
        playing = True
        loop_count = 0
        while playing:
            for i in range(100):
                self.farkle.randomize_dice()
                roll_score = self.farkle.score_roll(self.farkle.dice, self.farkle.reRoll)
                temp_memory = [self.farkle.dice, self.farkle.reRoll]
                reRoll = self.player.decide(self.farkle.reRoll, self.farkle.dice, self.tensor_session)
                # print("predicted", reRoll)
                # print("actual dice", self.farkle.dice)
                # if not reRoll.any():
                    # playing = False
                    # break
                fake_dice_roll = self.farkle.randomize_fake_dice(self.farkle.dice, reRoll)
                fake_score = self.farkle.score_roll(fake_dice_roll, [0, 0, 0, 0, 0, 0])

                # valid = self.farkle.is_valid_move(self.player.freeze(self.farkle.reRoll))  # random pick..don't use brain
                valid = self.farkle.is_valid_move(reRoll)  # player... use brain
                # print(valid)
                # Triggers if all the dice zero
                if not any(self.farkle.reRoll):
                    self.player.gameScore += self.player.roundScore + roll_score
                    self.player.roundScore = 0
                # If not all the dice are zero, it's not the end of a round
                else:
                    if valid and roll_score is not 0:
                        # Collect the points
                        self.player.roundScore += roll_score
                    else:
                        # Until we fail
                        self.player.roundScore = 0

                temp_memory.append(roll_score)
                temp_memory.append(fake_score)
                self.player.memory.add_sample(temp_memory)
            # WE NEED TO REPLAY AKA TRAIN
            self.player.train(self.tensor_session)
                # self.player.memory.
            # print(self.player.gameScore)
            average += self.player.gameScore
            loop_count += 1


            self.player.gameScore = 0

            if loop_count > 100:
                playing = False
        print("Average roll_score per game: " + str(average / loop_count))
