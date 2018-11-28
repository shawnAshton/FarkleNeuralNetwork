import rules
import greedy_player
import gameRunner
import greedy_player
import tensorflow as tf

if __name__ == "__main__":
    farkle = rules.Game()
    player = greedy_player.Player()
    not_greedy_player = greedy_player.Player()
    learning_rate_decay = 0.1
    learning_rate_start = 10
    learning_rate_min = 0.1

    with tf.Session() as tensor_session:
        runner = gameRunner.GameRunner(player, not_greedy_player, farkle, tensor_session,
                                           learning_rate_decay, learning_rate_start, learning_rate_min)
        runner.run()



# neural net in player...player methods
# replay method for the runner object - go back in memory and train yo self

# extra... work with the not greedy player