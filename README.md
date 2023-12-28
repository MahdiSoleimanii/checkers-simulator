# Checkers Simulator
Here we give an implementation of the Checkers game, where two bots play against each other.
below are the algorithms and techniques that are implemented:

## Min-Max Algorithm:
Each player (bot) uses this algorithm to decide its next move.

## Alpha-Beta Pruning:
This is used to speed up the Min-Max algorithm.

## Heuristic Function
This function is used to estimate the game status at any given depth so the Min-Max algorithm doesn't have to check the entire search space every time.
- Note that the heuristic function takes a `max_depth` as input so the player (bot) with higher depth makes better decisions.

## Forward Pruning
This technique is used to speed-up our algorithm so that we can increase the depth we can apply the heuristic function

***Forward Pruning***: is a method to decrease the number of nodes that are checked at each level in a search.
To prune the 'unpromising' nodes we can use an evaluation function or make use of a mechanical method like **Beam Search**.

## The Game
- The board is of size `8 × 8`.
- There is no input to the algorithm, since the start state of the game is always the same
