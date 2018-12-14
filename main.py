import rules
import gameRunner
import gameRunnerRandom
import gameRunnerPerfectRoll
import greedy_player
import tensorflow as tf

if __name__ == "__main__":
    farkle = rules.Game()
    player = greedy_player.Player()

    learning_rate_decay = .001
    learning_rate_start = 100
    learning_rate_min = 0.1

    with tf.Session() as tensor_session:
        init = tf.global_variables_initializer()
        tensor_session.run(init)
        runner = gameRunner.GameRunner(player, farkle, tensor_session,
                                           learning_rate_decay, learning_rate_start, learning_rate_min)
        runner.run()

    print("\n")
    farkle = rules.Game()
    player = greedy_player.Player()
    with tf.Session() as tensor_session:
        init = tf.global_variables_initializer()
        tensor_session.run(init)
        runner = gameRunnerRandom.GameRunner(player, farkle, tensor_session,
                                           learning_rate_decay, learning_rate_start, learning_rate_min)
        runner.run()

    print("\n")

    farkle = rules.Game()
    player = greedy_player.Player()
    with tf.Session() as tensor_session:
        init = tf.global_variables_initializer()
        tensor_session.run(init)
        runner = gameRunnerPerfectRoll.GameRunner(player, farkle, tensor_session,
                                           learning_rate_decay, learning_rate_start, learning_rate_min)
        runner.run()

