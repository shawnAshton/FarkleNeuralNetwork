import random
import model
import memory
import numpy as np
from sklearn import preprocessing

class Player:
    def __init__(self):
        self.gameScore = 0
        self.roundScore = 0
        self.neuralNet = model.Model(6, 6, 1000)
        self.memory = memory.Memory(80000)

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

        inputs = np.zeros((len(batch), self.neuralNet.num_states))
        outputs = np.zeros((len(batch), self.neuralNet.num_actions))
        for i, b in enumerate(batch):
            state, frozen_dice, cScore, pScore = b[0], b[1], b[2], b[3]
            inputs[i] = state
            # inputs[i] = state + frozen_dice
            single_target = [1, 1, 1, 1, 1, 1]
            if pScore <= cScore:
                if random.randint(0,1) == 0:
                    outputs[i] = [0, 0, 0, 0, 0, 0]
            else:
                for j, die in enumerate(state):
                    if state[j] is 1:
                        single_target[j] = 0
                    if state[j] is 2:
                        single_target[j] = 0

                outputs[i] = single_target
            # print("Dice in memory", state)
            # print("Current roll in memory", frozen_dice)
            # print("Target roll in memory", outputs[i])

        #  back propagate the score
        input_scaler = preprocessing.StandardScaler()
        input_scaler.fit(inputs)
        inputs = input_scaler.transform(inputs)
        output_scaler = preprocessing.StandardScaler()
        output_scaler.fit(outputs)
        outputs = output_scaler.transform(outputs)
        self.neuralNet.train_batch(sess, inputs, outputs)

    def decide(self, current_state, frozen_dice, sess):
        # greedy inputs...
        # state = current_state + frozen_dice
        state = current_state
        state = np.array(state)
        # Predict returns it in [[]] form. Get the 0th index to get just [] form.
        predicted_reRoll = self.neuralNet.predict_one(state, sess)[0]

        # We get decimals, round them to 0 or 1
        for i, die in enumerate(predicted_reRoll):
            predicted_reRoll[i] = round(predicted_reRoll[i])

        predicted_reRoll = [int(die) for die in predicted_reRoll]

        # outputs...
            # array of 6 zeros and ones...
        return predicted_reRoll
