from statistics import median

import rules
import greedy_player
import tensorflow as tf
import csv
import matplotlib.pyplot as plt

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
        game_count = 0
        total_score = 0
        max_game_score = 10000
        number_rounds = 0
        plot_game_score = []
        plot_number_rounds = []
        round_scores = []
        while playing:
            while self.player.gameScore < max_game_score:
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
                    final_round_score = self.player.roundScore + roll_score
                    round_scores.append(final_round_score)
                    self.player.gameScore += final_round_score
                    self.player.roundScore = 0
                    self.farkle.new_round = False
                    number_rounds += 1
                # If not all the dice are zero, it's not the end of a round
                else:
                    if roll_score is not 0:
                        # Collect the points
                        self.player.roundScore += roll_score
                    else:
                        # Until we fail
                        self.player.roundScore = 0

                temp_memory.append(roll_score)
                temp_memory.append(fake_score)
                self.player.memory.add_sample(temp_memory)

            plot_number_rounds.append(number_rounds)
            number_rounds = 0
            # WE NEED TO REPLAY AKA TRAIN
            self.player.train(self.tensor_session)
            total_score += self.player.gameScore
            plot_game_score.append(self.player.gameScore)
            self.player.gameScore = 0
            game_count += 1

            if game_count > 500:
                playing = False
        average_round_score_per_game = [plot_game_score[i] / plot_number_rounds[i] for i in range(len(plot_game_score))]
        # average_round_score_per_game = median(plot_game_score)
        print("median game score", median(plot_game_score))
        plt.plot(average_round_score_per_game)
        plt.title("Average round score per game")
        plt.ylabel("Average Round Score")
        plt.xlabel("Game Number")
        plt.show()
        plt.plot(plot_number_rounds)
        plt.title("Number of Rounds per Game")
        plt.ylabel("Number of Rounds")
        plt.xlabel("Game Number")
        plt.show()
        # plot.plot(plot_game_score)
        # plot.title("Game score over time")
        # plot.ylabel("Game Score")
        # plot.xlabel("Turn")
        # plot.show()
        print("Average roll_score per game with NN: " + str(total_score / (game_count * 100)))
        print("median round score with NN", median(round_scores))
