cScore = 300
pScore = 600
state = [2, 2, 1, 5, 3, 5]
frozen_dice = [1, 1, 0, 1, 1, 1]

# use state and frozen_dice....and anything else you can think of....
# make sure you do not roll more than you can..... count of frozen dice + 1 is the amount that has to be frozen
# you can roll less than this though...


outputs = [1, 1, 1, 1, 1, 1]

if pScore is None:
    pScore = cScore
    # current_q[frozen_dice] = cScore
else:
    if pScore <= cScore:
        outputs = [0, 0, 0, 0, 0, 0]
    else:
        #     find the number of tings we can actually reroll... + 1
        count_frozen_die = 0
        for die in frozen_dice:
            if die is 0:
                count_frozen_die += 1
        count_frozen_die += 1
        amount_to_reroll = 6 - count_frozen_die
        print(amount_to_reroll)
        single_target = [1, 1, 1, 1, 1, 1]
        count_of_target_frozen = 0
        for j, die in enumerate(state):
            if frozen_dice[j] == 0:
                single_target[j] = 0
                count_of_target_frozen += 1
            elif die is 1 and count_of_target_frozen <= amount_to_reroll:
                single_target[j] = 0
                count_of_target_frozen += 1

        for j, die in enumerate(state):
            if frozen_dice[j] == 0:
                single_target[j] = 0
                count_of_target_frozen += 1
            elif die is 5 and count_of_target_frozen <= amount_to_reroll:
                single_target[j] = 0
                count_of_target_frozen += 1
        outputs = single_target
print(outputs)
