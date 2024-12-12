# 2024 Fall Final Project - X-game

The work was collaborated by Jiachen Yu(jy91) and YouPeng(youpeng2). I was responsible for basic game modeling, and YouPeng tried more about the game strategy(like the Menace).

X, by Mark Steere, is a three player game played on a diamond shaped board with a hexagonal pattern. An introduction pdf can be found in https://www.marksteeregames.com/X_rules.pdf.

## Result
<img width="388" alt="image" src="https://github.com/user-attachments/assets/b4e324f7-37ee-4fcf-bfb7-4566fe1869b5">

The detailed implementation function is in def display_board(self).

## Code Implementation 
All the functions end with "_updated" have the similar functionality with the original functions, but only the returns are different.

### Board Modeling
<img width="388" alt="image" src="https://github.com/user-attachments/assets/804e9899-0395-4d56-8e67-e286b5d0cd69">

Above is one example for the board modeling. In the example, column -6 and -5 are marked by the dotted lines. In each column, the y starts from 0. The x, ranging from -7 to 7, in the middle column is 0. The detailed implementation is in def __init__(self, size).

### Corner Claim Judgement  
<img width="309" alt="image" src="https://github.com/user-attachments/assets/b55e45dc-139a-48c4-b68e-752a70512029">

def find_path(self, x, y) and def check_ending_value(self) are used to solve the corner claim problem. Here we used the width-first search algorithm to find all the paths starting from the given cell and ending at the edge, and the find_path will return the set of all the ending edges. To update the corner claims dictionary, we only need to check paths of all the cells on edge1 and edge2 to know about all the four corners. The complexity of solving one corner claim is O(n^2)(n is the length of the edge), since in the worst situation, it has to traverse all the paths starting from a specific edge.


### Menace For Orginal Xgame

def check_game_result(self) and its updated function are used to find the winner when the game is end. The winner is based on corner control and game state.

When during the AI learning processing, we use a dictionary to "simulate" the matchbox, each different boards and possible next moves are recorded as different "KEY" and "Value".

def change_matchbox(self) will update the weights according to the game result.

### Orginal Xgame Result.

We ran two separate simulations, the first one used 150,000 simulations and the overall win rate was above 40% and it looked like it was trending upwards, then we ran another one million simulations, at this point our model's win rate became much higher, but what we can notice is that the increase in his win rate is very low. While it may be possible to have a very high win rate using this method in the future, it would require a very large amount of computation.

### Updated Xgame
We made a little bit change to the xgame so that instead of deciding who won the game by the number of node controls, we used the way that the person with the largest number of controls won the game.

### Updated Xgame Result.
The results this time are actually very similar to the previous ones, and considering that this is a three-player game, an accuracy of roughly 40 or more is already a relatively good result. After a million simulations, our ai player has a slightly higher win rate than our original xgame's ai player. And it is worth noting that in our new and improved xgame, there are some game will end with "Draw". So this result may actually be a bit higher than the win rate.

### Future work & Limitation
#### Long Training Time 
MENACE (Matchbox Educable Noughts and Crosses Engine) requires a considerable amount of time and attempts to learn all possible states due to its state enumeration-based training method. It is not feasible to trace all cases, and the sample size near the final decision points is very small.
#### Expanding the Game Concept 
Transitioning from an edge-length-based coverage model to a more comprehensive model that focuses on enclosed hexcells formed by every two edges. The goal is to maximize the total area captured, introducing a new strategy. The increased complexity means that larger areas yield higher rewards, requiring more sophisticated decision-making. This demands optimization of both the placement and connection of edges, leading to significantly higher computational demands due to the exponential growth in possible area combinations.