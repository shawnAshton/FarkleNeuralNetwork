import game
import greedy_player


if __name__ == "__main__":
    farkle = game.Game()
    player = greedy_player.Player()
    average = 0
    for j in range(100):
        score = 0
        for i in range(100):
            farkle.randomize_dice()
            score = farkle.score_roll()
            valid = farkle.is_valid_move(player.freeze(farkle.frozen))

            # Triggers if all the dice zero
            if not any(farkle.frozen):
                player.totalScore += player.roundScore + score
                player.roundScore = 0
            # If not all the dice are zero, it's not the end of a round
            else:
                if valid and score is not 0:
                    # Collect the points
                    player.roundScore += score
                else:
                    # Until we fail
                    player.roundScore = 0
        print(player.totalScore)
        average += player.totalScore
        player.totalScore = 0
    print("Average score per game: " + str(average / 100))
