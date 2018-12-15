import random

from collections import Counter

import model
import memory
import numpy as np

class Player:
    def __init__(self):
        self.gameScore = 0
        self.roundScore = 0
        self.neuralNet = model.Model(12, 6, 500)
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

    def perfect_roll(self, state):
        single_target = [1, 1, 1, 1, 1, 1]
        for j, die in enumerate(state):
            if state[j] is 2:
                single_target[j] = 0
            if state[j] is 1:
                single_target[j] = 0

            # checking triples
            how_many_state = Counter(state)
            # print(state)
            for k in range(0, 6):
                # print(how_many_state[5])

                if how_many_state[k] >= 3:
                    for l in range(0, len(state)):
                        if state[l] is k:
                            single_target[l] = 0

            # but should you really roll?
            single_target_count = Counter(single_target)
            if single_target_count[1] < 3:
                single_target = [0, 0, 0, 0, 0, 0]
        return single_target

    # def perfect_roll(self, state, frozen):          whatever is frozen must stay frozen...
    #     count_of_needed_frozen = 0
    #     for i, game_die in enumerate(frozen):
    #         if game_die == 0:
    #             count_of_needed_frozen += 1
    #     count_of_needed_frozen += 1
    #
    #     single_target = [1, 1, 1, 1, 1, 1]
    #     for j, die in enumerate(state):
    #         if state[j] is 2:
    #             single_target[j] = 0
    #         if state[j] is 1:
    #             single_target[j] = 0
    #
    #         # checking triples
    #         how_many_state = Counter(state)
    #         # print(state)
    #         for k in range(0, 6):
    #             # print(how_many_state[5])
    #
    #             if how_many_state[k] >= 3:
    #                 for l in range(0, len(state)):
    #                     if state[l] is k:
    #                         single_target[l] = 0
    #
    #         # but should you really roll?
    #         single_target_count = Counter(single_target)
    #         if single_target_count[1] < 3:
    #             single_target = [0, 0, 0, 0, 0, 0]
    #
    #     count_of_actual_frozen = 0
    #     for i, game_die in enumerate(single_target):
    #         if game_die == 0:
    #             count_of_actual_frozen += 1
    #     # print("\n\n\n")
    #     while count_of_needed_frozen > count_of_actual_frozen:  # freeze one more
    #         # print("stuck")
    #         made_single_change = False
    #         for i, game_die in enumerate(single_target):
    #             if game_die == 1 and (not made_single_change):
    #                 single_target[i] = 0
    #                 made_single_change = True
    #                 count_of_needed_frozen -= 1
    #     # print("\n\n\n")
    #     return single_target

    # def better_perfect_roll(self, state, frozen):
    #     to_return = [1, 1, 1, 1, 1, 1]
    #     count_of_frozen = 0
    #     for i, game_die in enumerate(frozen):
    #         if game_die == 0:
    #             to_return[i] = 0
    #             count_of_frozen += 1
    #     count_of_frozen += 1
    #     count_of_things_i_can_change = 6 - count_of_frozen
    #     changes_ive_made = 0
    #     if count_of_things_i_can_change < 3:
    #         to_return = [0, 0, 0, 0, 0, 0]
    #     else:
    #         for j, die in enumerate(state):
    #             if state[j] is 2:
    #                 if to_return[j] == 1:
    #                     to_return[j] = 0
    #                     changes_ive_made += 1
    #             if state[j] is 1:
    #                 if to_return[j] == 1:
    #                     to_return[j] = 0
    #                     changes_ive_made += 1
    #
    #     if changes_ive_made > 0:
    #         return to_return
    #     else:  # I must make a change
    #         for i, game_die in enumerate(frozen):
    #             if game_die == 1:
    #                 to_return[i] = 0
    #                 return to_return


    def train(self, sess):
        # note: model = nn
        batch = self.memory.sample(self.neuralNet.batch_size) # samples your memory... then trains based on what it knows...

        inputs = np.zeros((len(batch), self.neuralNet.num_states))
        outputs = np.zeros((len(batch), self.neuralNet.num_actions))
        for i, b in enumerate(batch):
            state, frozen_dice, cScore, pScore = b[0], b[1], b[2], b[3]
            inputs[i] = state + frozen_dice
            single_target = [1, 1, 1, 1, 1, 1]
            if pScore <= cScore:
                outputs[i] = [0, 0, 0, 0, 0, 0]
            else:
                for j, die in enumerate(state):
                    if state[j] is 2:
                        single_target[j] = 0
                    if state[j] is 1:
                        single_target[j] = 0

                    # checking triples
                    how_many_state = Counter(state)
                    # print(state)
                    for k in range(0, 6):
                        # print(how_many_state[5])

                        if how_many_state[k] >= 3:
                            for l in range(0, len(state)):
                                if state[l] is k:
                                    single_target[l] = 0

                    # but should you really roll?
                    single_target_count = Counter(single_target)
                    if single_target_count[1] < 2:
                        single_target = [0, 0, 0, 0, 0, 0]

                outputs[i] = single_target
            # print("Dice in memory", state)
            # print("Current roll in memory", frozen_dice)
            # print("Target roll in memory", outputs[i])

        #  back propagate the score
        self.neuralNet.train_batch(sess, inputs, outputs)

    def decide(self, current_state, frozen_dice, sess):
        # greedy inputs...
        state = current_state + frozen_dice
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
