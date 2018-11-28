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
                score = self.farkle.score_roll()
                valid = self.farkle.is_valid_move(self.player.freeze(self.farkle.frozen))
                # Triggers if all the dice zero
                if not any(self.farkle.frozen):
                    self.player.gameScore += self.player.roundScore + score
                    self.player.roundScore = 0
                # If not all the dice are zero, it's not the end of a round
                else:
                    if valid and score is not 0:
                        # Collect the points
                        self.player.roundScore += score
                    else:
                        # Until we fail
                        self.player.roundScore = 0
            if self.player.gameScore:
                print(self.player.gameScore)
                average += self.player.gameScore
                loop_count += 1
            self.player.gameScore = 0
            if loop_count > 100:
                playing = False
        print("Average score per game: " + str(average / loop_count))
