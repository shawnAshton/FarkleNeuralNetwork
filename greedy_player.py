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
        # note: model = nn
        batch = self.memory.sample(self.neuralNet.batch_size) # samples your memory... then trains based on what it knows...
        # states = np.array([val[0] for val in batch])
        # next_states = np.array([(np.zeros(self._model.num_states)
        #                          if val[3] is None else val[3]) for val in batch])
        # q_s_a = self._model.predict_batch(states, self._sess)
        # q_s_a_d = self._model.predict_batch(next_states, self._sess)
        inputs = np.zeros((len(batch), self.neuralNet.num_states))
        outputs = np.zeros((len(batch), self.neuralNet.num_actions))
        for i, b in enumerate(batch):
            state, frozen_dice, cScore, pScore = b[0], b[1], b[2], b[3]
            inputs[i] = state + frozen_dice

            if pScore <= cScore:
                outputs[i] = [0, 0, 0, 0, 0, 0]
            else:
            #     find the number of tings we can actually reroll... + 1
                count_frozen_die = 0
                for die in frozen_dice:
                    if die is 0:
                        count_frozen_die += 1
                count_frozen_die += 1
                amount_to_reroll = 6 - count_frozen_die
                single_target = [1,1,1,1,1,1]
                count_of_target_frozen = 0
                for j, die in enumerate(state):
                    if frozen_dice[j] == 0:
                        single_target[j] = 0
                        count_of_target_frozen += 1
                    elif die is 1 and count_of_target_frozen < amount_to_reroll:
                        single_target[j] = 0
                        count_of_target_frozen += 1

                for j, die in enumerate(state):
                    if frozen_dice[j] == 0:
                        single_target[j] = 0
                        count_of_target_frozen += 1
                    elif die is 5 and count_of_target_frozen < amount_to_reroll:
                        single_target[j] = 0
                        count_of_target_frozen += 1
                outputs[i] = single_target

        #    THINKING OF current scores and potential scores... if statements..? looking at the replay function of 2nd link
        #  also... we are here cause we think we need to add to memory b4 we can decide...
        # pytorch..?


        # self.neuralNet.train_batch(sess,states,rewards)


        # use the memory to train the Neural Network
            #  INPUTS
            #  current_state (array)
            #  our frozen_dice (array of zero and ones)

            #  back propagate the score
        self.neuralNet.train_batch(sess, inputs, outputs)

    def decide(self, current_state, frozen_dice, sess):
        # greedy inputs...
        state = current_state + frozen_dice
        state = np.array(state)
        # Predict returns it in [[]] form. Get the 0th index to get just [] form.
        something = self.neuralNet.predict_one(state, sess)[0]
        print(something)
        # We get decimals, round them to 0 or 1
        for i, die in enumerate(something):
            something[i] = round(something[i])

        print(something)
        # print(type(something))
            #  current_state (array)
            #  our frozen_dice (array of zero and ones)

        # use the neural net to decide what to do..
            # create NeuralNet

        # outputs...
            # array of 6 zeros and ones...
        return something
