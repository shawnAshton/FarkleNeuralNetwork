import random
import model
import memory
import numpy as np

class Player:
    def __init__(self):
        self.gameScore = 0
        self.roundScore = 0
        self.neuralNet = model.Model(12, 6, 6)
        self.memory = memory.Memory(800)

    def freeze(self, frozen):
        """
            randomly freezes valid dice, so that they will not be rolled again...this is a test function... not used
            for neural net...
        """
        freeze_dice = []
        for i in range(6):
            if frozen[i] is 1:  #
                freeze_dice.append(random.randint(0, 1))
            else:
                freeze_dice.append(0)
        return freeze_dice

    def train(self, sess):
        # model -> nn
        # remove underscore in memory
        batch = self._memory.sample(self._model.batch_size)
        states = np.array([val[0] for val in batch])
        next_states = np.array([(np.zeros(self._model.num_states)
                                 if val[3] is None else val[3]) for val in batch])
        q_s_a = self._model.predict_batch(states, self._sess)
        q_s_a_d = self._model.predict_batch(next_states, self._sess)
        x = np.zeros((len(batch), self._model.num_states))
        y = np.zeros((len(batch), self._model.num_actions))
        for i, b in enumerate(batch):
            state, frozen_dice, cScore, pScore = b[0], b[1], b[2], b[3]
            current_q = q_s_a[i]
            if pScore is None:
                pScore = cScore
                current_q[frozen_dice] = cScore
            else:
                current_q[frozen_dice] = pScore
        #    THINKING OF current scores and potential scores... if statements..? looking at the replay function of 2nd link
        #
        # pytorch..?












        # use the memory to train the Neural Network
            #  INPUTS
            #  current_state (array)
            #  our frozen_dice (array of zero and ones)

            #  back propagate the score
        return 4

    def decide(self, current_state, frozen_dice, sess):
        # greedy inputs...
        state = current_state + frozen_dice
        state = np.array(state)
        something = self.neuralNet.predict_one(state, sess)
        # print(something)
        # print(type(something))
            #  current_state (array)
            #  our frozen_dice (array of zero and ones)

        # use the neural net to decide what to do..
            # create NeuralNet

        # outputs...
            # array of 6 zeros and ones...
        return [0, 0, 0, 0, 0, 0]
