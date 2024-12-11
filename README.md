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

Above is one example for the board modeling. 
From the example above, column -6 and -5 are marked by the dotted lines. In each column, the y starts from 0. The x, ranging from -7 to 7, in the middle column is 0. The detailed implementation is in def __init__(self, size).

### Corner Claim Judgement  
<img width="309" alt="image" src="https://github.com/user-attachments/assets/b55e45dc-139a-48c4-b68e-752a70512029">

def find_path(self, x, y) and def check_ending_value(self) are used to solve the corner claim problem. Here we used the width-first search algorithm to find all the paths starting from the given cell and ending at the edge, and the find_path will return the set of all the ending edges. To update the corner claims dictionary, we only need to check paths of all the cells on edge1 and edge2 to know about all the four corners. The complexity of solving one corner claim is O(n^2)(n is the length of the edge), since in the worst situation, it has to traverse all the paths starting from a specific edge.


