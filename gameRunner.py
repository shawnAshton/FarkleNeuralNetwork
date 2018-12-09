import rules
import greedy_player
import tensorflow as tf
import matplotlib.pyplot as plot

class GameRunner:
    def __init__(self, player, farkle, tensor_session, learning_rate_decay, learning_rate_start, learning_rate_min):
        self.player = player
        self.farkle = farkle
        self.tensor_session = tensor_session
        self.learning_rate_decay = learning_rate_decay
        self.learning_rate_start = learning_rate_start
        self.learning_rate_min = learning_rate_min

    def run(self):
        playing = True
        loop_count = 0
        total_score = 0
        plot_game_score = []
        while playing:
            for i in range(100):
                self.farkle.randomize_dice()
                valid = False
                # The player makes a decision:
                reRoll = self.player.decide(self.farkle.dice, self.farkle.reRoll, self.tensor_session)
                while not valid:
                    valid = self.farkle.is_valid_move(reRoll)  # player... use brain
                    if any(reRoll):
                        if valid:
                           self.farkle.set_reRoll(reRoll)
                        else:
                            reRoll = self.farkle.randomize_frozen()

                roll_score = self.farkle.score_roll(self.farkle.dice, self.farkle.reRoll)
                temp_memory = [self.farkle.dice, self.farkle.reRoll]

                fake_dice_roll = self.farkle.randomize_fake_dice(self.farkle.dice, reRoll)
                fake_score = self.farkle.score_roll(fake_dice_roll, [0, 0, 0, 0, 0, 0])

                # Triggers if all the dice zero
                if self.farkle.new_round:
                    self.player.gameScore += self.player.roundScore + roll_score
                    self.player.roundScore = 0
                    self.farkle.new_round = False
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
            total_score += self.player.gameScore
            plot_game_score.append(self.player.gameScore)
            self.player.gameScore = 0
            loop_count += 1

            if loop_count > 1000:
                playing = False
        plot.plot(plot_game_score)
        plot.title("Game score over time")
        plot.ylabel("Game Score")
        plot.xlabel("Turn")
        plot.show()
        print("Average roll_score per game: " + str(total_score / (loop_count * 100)))
