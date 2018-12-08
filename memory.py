import random

###########################################################################
#   a player can train based on their memory.
#   memory is created with samples...
#       2 dimensional array... with many rows of state, and Round score
###########################################################################
class Memory:
    def __init__(self, max_memory):
        self._max_memory = max_memory
        self._samples = []

    def add_sample(self, sample):  # state, frozen dice, cscore, pscore
        self._samples.append(sample)
        if len(self._samples) > self._max_memory:  # if we don't have space.. pop some memory...
            self._samples.pop(0)

    def sample(self, num_samples):
        if num_samples > len(self._samples): # if you want to sample more than I know....
            return random.sample(self._samples, len(self._samples))  # i'll tell ya everything...
        else:
            return random.sample(self._samples, num_samples)         # i'll give ya what ya want

