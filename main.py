import rules
import gameRunner
import gameRunnerRandom
import gameRunnerPerfectRoll
import greedy_player
import tensorflow as tf
tf.compat.v1.disable_eager_execution()
# import tensorflow as tf

if __name__ == "__main__":
    farkle = rules.Game()
    player = greedy_player.Player()


    with tf.compat.v1.Session() as tensor_session:
        init = tf.compat.v1.global_variables_initializer()
        tensor_session.run(init)
        runner = gameRunner.GameRunner(player, farkle, tensor_session)
        runner.run()

    # print("\n")
    # farkle = rules.Game()
    # player = greedy_player.Player()
    # with tf.Session() as tensor_session:
    #     init = tf.global_variables_initializer()
    #     tensor_session.run(init)
    #     runner = gameRunnerRandom.GameRunner(player, farkle, tensor_session)
    #     runner.run()

    # print("\n")
    #
    # farkle = rules.Game()
    # player = greedy_player.Player()
    # with tf.Session() as tensor_session:
    #     init = tf.global_variables_initializer()
    #     tensor_session.run(init)
    #     runner = gameRunnerPerfectRoll.GameRunner(player, farkle, tensor_session)
    #     runner.run()

