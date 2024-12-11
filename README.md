# 2024 Fall Final Project - X-game

The work was collaborated by Jiachen Yu(jy91) and YouPeng(youpeng2). I was responsible for basic game modeling, and YouPeng tried more about the game strategy(like the Menace).

X, by Mark Steere, is a three player game played on a diamond shaped board with a hexagonal pattern. An introduction pdf can be found in https://www.marksteeregames.com/X_rules.pdf.

## Result
<img width="388" alt="image" src="https://github.com/user-attachments/assets/b4e324f7-37ee-4fcf-bfb7-4566fe1869b5">

The detailed implementation function is in def display_board(self).

## Code Implementation 
### Board Modeling
Here is the detail for the board modeling. 
<img width="629" alt="image" src="https://github.com/user-attachments/assets/804e9899-0395-4d56-8e67-e286b5d0cd69">
From the example above, column -6 and -5 are marked by the dotted lines. In each column, the y starts from 0. The x, ranging from -7 to 7, in the middle column is 0. The detailed implementation is in def __init__(self, size).

### Corner Claim Judgement  
<img width="309" alt="image" src="https://github.com/user-attachments/assets/b55e45dc-139a-48c4-b68e-752a70512029">


