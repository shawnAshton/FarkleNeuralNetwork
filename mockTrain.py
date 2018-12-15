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
    else if pScore <= cScore + 100:


print(outputs)
