import rules
import greedy_player
import tensorflow as tf

class GameRunner:
    def __init__(self, player, not_greedy_player, farkle, tensor_session, learning_rate_decay, learning_rate_start, learning_rate_min):
        self.player = player
        self.farkle = farkle
        self.not_greedy_player = not_greedy_player
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
                roll_score = self.farkle.score_roll()
                temp_memory = [self.farkle.dice, self.farkle.reRoll]

                # valid = self.farkle.is_valid_move(self.player.freeze(self.farkle.reRoll))  # random pick..don't use brain
                valid = self.farkle.is_valid_move(self.player.decide(self.farkle.reRoll, self.farkle.dice, self.tensor_session))  # player... use brain
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
                        roll_score = -3000
                temp_memory.append(roll_score)

            print(self.player.gameScore)
            average += self.player.gameScore
            loop_count += 1

                # self.player.memory.add_sample()
            self.player.gameScore = 0
            if loop_count > 100:
                playing = False
        print("Average roll_score per game: " + str(average / loop_count))
