import random
import matplotlib as plt
import pandas as pd
import matplotlib.pyplot as plt
#When testing, fix the random seed to get the same result
random.seed(102 )
matchbox_sets = {}
WIN = 2
LOSE = -1
DRAW = 1
class XGame:
    def __init__(self, size):
        """
        Initialize the game with a hexagonal board and player settings.
        """
        # For the fairness of the game, the size should be a multiple of 3 
        assert size % 3 == 0, "The size of the board should be a multiple of 3."
        self.size = size # The length of the edge of the hexagon
        self.board = self._initialize_board()
        self.players = ['Red', 'Yellow', 'Green']
        self.next_player_index = 0  # Red starts
        self.corner_claims = {player: set() for player in self.players}
        self.value = {
            (-5, 0): 2,
            (0, 0): 2,
            (0, 5): 2,
            (5, 0): 2
        }
        self.moves_made = 0

        # Use sets to store 4 edges
        self.four_edges = []
        edge0 = set((x, 0) for x in range(-size + 1, 1))
        edge1 = set((x, self.size - abs(x) - 1) for x in range(-size + 1, 1))
        edge2 = set((x, 0) for x in range(0, size))
        edge3 = set((x, self.size - abs(x) - 1) for x in range(0, size))
        self.four_edges.extend([edge0, edge1, edge2, edge3])
        

    def _initialize_board(self):
        """
        :return: A dictionary where keys are (x, y) tuples and values are None (unclaimed cells).
        """
        board = {}
        max_x = self.size - 1
        for x in range(-max_x, max_x + 1):
            max_y = self.size - abs(x) - 1
            for y in range(0, max_y + 1):
                board[(x, y)] = None
        return board

    def display_board(self):
        """
        Displays the hexagonal board in a diamond shape with colored chess pieces.
        """       
        size = self.size
        max_x = size - 1
        num_rows = 2 * size - 1
        # self.board[(0, 0)] = 'Green'
        # self.board[(0, 1)] = 'Red'
        # self.board[(0, 2)] = 'Yellow'

        # ANSI color codes
        color_codes = {
            'Red': '\033[31m',
            'Yellow': '\033[33m',
            'Green': '\033[32m',
            None: '\033[30m'  # Black for unclaimed cells
        }
        reset_code = '\033[0m'

        for display_row in range(num_rows):
            x = display_row - max_x
            max_y = size - abs(x) - 1
            y_values = range(0, max_y + 1)

            # Print leading spaces for indentation
            # a small hexagonal chess takes 2 spaces to help with the diamond shape
            print(' ' * abs(x), end='')

            for y in y_values:
                cell = self.board.get((x, y), None)
                color = color_codes.get(cell, '\033[30m')  # Default to black if color not found
                # Inserts the ANSI escape code
                print(f'{color}●{reset_code} ', end='')

            print()
    
    def _get_neighbors(self, x, y, color):
        """
        Get the neighbors with the same color of the given cell.
        """
        if color is None:
            return []
        # Left diamond
        if x < 0:
            neighbors = []
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (-1, -1), (1, 0), (1, 1)]:
                neighbor = (x + dx, y + dy)
                if neighbor in self.board and self.board[neighbor] == color:    
                    neighbors.append(neighbor)
        # Right diamond
        if x > 0:
            neighbors = []
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (-1, 1), (1, 0), (1, -1)]:
                neighbor = (x + dx, y + dy)
                if neighbor in self.board and self.board[neighbor] == color:
                    neighbors.append(neighbor)
        # Middle diamond
        if x == 0:
            neighbors = []
            for dx, dy in [(0, -1), (0, 1), (-1, -1), (-1, 0), (1, -1),(1, 0)]:
                neighbor = (x + dx, y + dy)
                if neighbor in self.board and self.board[neighbor] == color:
                    neighbors.append(neighbor)
        return neighbors

    def _check_edge_cell(self, x, y):   
        """
        Check if the cell is on the edge.
        If it is, return the indexes of ending edges. Can be multiple because of the 4 corners!
        """
        ending_edges = set() 
        for i, edge in enumerate(self.four_edges):
            if (x, y) in edge:
                ending_edges.add(i)
        return ending_edges 
    
    def _check_edge_cell_update(self, x, y):

        ending_edges = {}
        edges = set()

        for i, edge in enumerate(self.four_edges):
            if (x, y) in edge:
                edges.add(i)

        if edges:
            ending_edges[(x, y)] = edges  # 以坐标为键，边索引集合为值

        return ending_edges

    def find_path(self, x, y):
        """
        Find all the path starting from the given cell and ending at the edge.
        Use the width-first search algorithm.
        Return the set of all the ending edges.
        """
        if self.board[(x, y)] is None:
            return set()
        
        queue = [(x, y)]
        visited = set()
        ending_edges = set()

        visited.add((x, y))
        # Check if the starting cell is one of the four corners!
        ending_edge = self._check_edge_cell(x, y)
        if ending_edge:
            ending_edges.update(ending_edge)
        while queue:
            current = queue.pop(0)
            for neighbor in self._get_neighbors(current[0], current[1], self.board[current]):
                ending_edge = self._check_edge_cell(neighbor[0], neighbor[1])
                if ending_edge:
                    ending_edges.update(ending_edge)
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
        
        return ending_edges
    
    def find_path_updated(self, x, y):
        """
        Find all the path starting from the given cell and ending at the edge.
        Use the width-first search algorithm.
        Return the set of all the ending edges.
        """
        if self.board[(x, y)] is None:
            return set()
        
        queue = [(x, y)]
        visited = set()
        ending_coords = {} 

        visited.add((x, y))
        # Check if the starting cell is one of the four corners!

        edge_dict = self._check_edge_cell_update(x, y)  # 返回 {坐标: 边索引集合}
        for coord, edges in edge_dict.items():
            if coord not in ending_coords:
                ending_coords[coord] = set()
            ending_coords[coord].update(edges)  # 添加边索引集合
        while queue:
            current = queue.pop(0)
            for neighbor in self._get_neighbors(current[0], current[1], self.board[current]):
                ending_edge = self._check_edge_cell_update(neighbor[0], neighbor[1])
                if ending_edge:
                    ending_coords.update(ending_edge)
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
        
        return ending_coords
    
    def check_corner_claims(self):
        """
        Check for corner claims and update the corner claims dictionary.
        To check for four corner claims, we only need to check paths of all the cells on edge1 and edge2.
        """
        edge1_ending_edges = dict()
        edge2_ending_edges = dict()
        for x, y in self.four_edges[1]:
            ending_edges = self.find_path(x, y)
            edge1_ending_edges[(x, y)] = ending_edges
        for x, y in self.four_edges[2]:
            ending_edges = self.find_path(x, y)
            edge2_ending_edges[(x, y)] = ending_edges
        # Check for the corner(-size + 1, 0), from edge1 to edge0
        # the x should decrease from 0 to -size + 1
        for x in range(0, -self.size, -1):
            y = self.size - abs(x) - 1
            if 0 in edge1_ending_edges[(x, y)]:
                self.corner_claims[self.board[(x, y)]].add((-self.size + 1, 0))
                break
        # Check for the corner(0, size-1), from edge1 to edge3
        # the x should increase from -size + 1 to 0
        for x in range(-self.size + 1, 1):
            y = self.size - abs(x) - 1
            if 3 in edge1_ending_edges[(x, y)]:
                self.corner_claims[self.board[(x, y)]].add((0, self.size - 1))
                break
        # Check for the corner(0, 0), from edge2 to edge0
        # the x should decrease from size - 1 to 0
        for x in range(self.size - 1, -1, -1):
            y = 0
            if 0 in edge2_ending_edges[(x, y)]:
                self.corner_claims[self.board[(x, y)]].add((0, 0))
                break
        # Check for the corner(size-1, 0), from edge2 to edge3
        # the x should increase from 0 to size - 1
        for x in range(0, self.size):
            y = 0
            if 3 in edge2_ending_edges[(x, y)]:
                self.corner_claims[self.board[(x, y)]].add((self.size - 1, 0))
                break
    def check_ending_value(self):
        """
        Check for corner claims and update the corner claims dictionary.
        To check for four corner claims, we only need to check paths of all the cells on edge1 and edge2.
        """
        edge1_ending_edges = dict()
        edge2_ending_edges = dict()
        for x, y in self.four_edges[1]:
            ending_edges = self.find_path_updated(x, y)
            edge1_ending_edges[(x, y)] = ending_edges
        for x, y in self.four_edges[2]:
            ending_edges = self.find_path_updated(x, y)
            edge2_ending_edges[(x, y)] = ending_edges
        # Check for the corner(-size + 1, 0), from edge1 to edge0
        # the x should decrease from 0 to -size + 1
        # Left
        for x in range(0, -self.size, -1):
            y = self.size - abs(x) - 1
            # print(edge1_ending_edges[(x, y)])
            end_points = [key for key, value in edge1_ending_edges[(x, y)].items() if 0 in value]

            if end_points:
                
                self.corner_claims[self.board[(x, y)]].add((-self.size + 1, 0))
                self.value[(-5,0)] = 12+x+max(key[0] for key in end_points)

                break
        # Check for the corner(0, size-1), from edge1 to edge3
        # the x should increase from -size + 1 to 0
        # Top
        for x in range(-self.size + 1, 1):
            y = self.size - abs(x) - 1
            end_points = [key for key, value in edge1_ending_edges[(x, y)].items() if 3 in value]
            if end_points:

                self.corner_claims[self.board[(x, y)]].add((0, self.size - 1))
                self.value[(0,5)] = 2-x+max(key[0] for key in end_points)
                break
        # Check for the corner(0, 0), from edge2 to edge0
        # the x should decrease from size - 1 to 0
        #Bottom
        for x in range(self.size - 1, -1, -1):
            y = 0
            end_points = [key for key, value in edge2_ending_edges[(x, y)].items() if 0 in value]

            if end_points:
                self.corner_claims[self.board[(x, y)]].add((0, 0))
                self.value[(0,0)] = x + 2 - min(key[0] for key in end_points)

                break
        # Check for the corner(size-1, 0), from edge2 to edge3
        # the x should increase from 0 to size - 1
        #Right
        for x in range(0, self.size):
            y = 0
            end_points = [key for key, value in edge2_ending_edges[(x, y)].items() if 3 in value]

            if end_points:
                self.corner_claims[self.board[(x, y)]].add((self.size - 1, 0))
                self.value[(5,0)] = 12-x-min(key[0] for key in end_points)
                print(self.value)
                break

    def check_game_result(self):
        """
        At the end of the game, check for the winner by evaluating corner claims.
        """
        # print(self.board)
        total_cells = len(self.board)
        # print(total_cells)
        if self.moves_made < total_cells:
            # print(f"Game is not over yet. {total_cells - self.moves_made} moves left. Here is the current board:")
            # self.display_board()
            return None
        
        if self.moves_made == total_cells:
        #     self.display_board()
            # for player, corners in self.corner_claims.items():
            #     print(f"{player} has claimed corners: {corners}") 

            scores = {player: len(corners) for player, corners in self.corner_claims.items()}  
            # Check for the winner, the winner is the player with the maximum unique number of corners
            max_score = max(scores.values())
            winner = None
            if max_score > 2:
                winner = [player for player, score in scores.items() if score == max_score][0]
            if max_score == 2:
               for player, score in scores.items():
                   if score == 0:
                       winner = player
                       break #0 must be the winner
                   if score == 2:
                       winner = player # check if there is 0
            print(f"Game Over! Winner: {winner}")
            return winner
        
    def check_game_result_updated(self):
        """
        At the end of the game, check for the winner by evaluating corner claims.
        """
        # print(self.board)
        total_cells = len(self.board)
        # print(total_cells)
        if self.moves_made < total_cells:
            # print(f"Game is not over yet. {total_cells - self.moves_made} moves left. Here is the current board:")
            # self.display_board()
            return None
        
        if self.moves_made == total_cells:
        #     self.display_board()
            # for player, corners in self.corner_claims.items():
                # print(f"{player} has claimed corners: {corners}") 
            scores = {player: sum(self.value[c] for c in corners) for player, corners in self.corner_claims.items()}

            # Check for the winner, the winner is the player with the maximum unique number of corners
            max_score = max(scores.values())
            # for player, score in scores.items():
            #     print(f"{player} score is : {score}")
            winners = [player for player, score in scores.items() if score == max_score]
            if len(winners) == 1:
                return winners[0]  # 返回唯一赢家
            else:
                return "Draw"  # 返回平局
            # winner = None
            # if max_score > 2:
            #     winner = [player for player, score in scores.items() if score == max_score][0]
            # if max_score == 2:
            #    for player, score in scores.items():
            #        if score == 0:
            #            winner = player
            #            break #0 must be the winner
            #        if score == 2:
            #            winner = player # check if there is 0
            # # print(f"Game Over! Winner: {winner}")
            return 1
    def make_move(self, x, y):
        """
        :return: True if the move is successful, False otherwise.
        """
        if (x, y) not in self.board:
            # print(f"Invalid move: {x, y} is not a valid position.")
            return False
        if self.board[(x, y)] is not None:
            # print(f"Invalid move: {x, y} already occupied.")
            return False

        # Make the move
        current_player = self.players[self.next_player_index]
        self.board[(x, y)] = current_player
        self.moves_made += 1

        # Update the turn
        self.next_player_index = (self.next_player_index + 1) % len(self.players)
        return True

    def make_moves(self, moves):
        """
        Make a series of moves.
        :param moves: A list of (x, y) tuples.
        """
        for x, y in moves:
            self.make_move(x, y)

        # self.display_board()    
        self.check_corner_claims()
        # for player, corners in self.corner_claims.items():
        #     print(f"{player} has claimed corners: {corners}")                 

    def generate_random_moves(self, num_moves):
        """
        Generate random moves for the game.
        """
        moves = []
        while len(moves) < num_moves:
            x = random.randint(-self.size + 1, self.size - 1)
            max_y = self.size - abs(x) - 1
            y = random.randint(0, max_y)
            if (x,y) not in moves:
                moves.append((x, y))
                self.make_move(x,y)
        return moves
    
    
    def generate_random_1move(self, moves):
        """
        Generate random moves for the other two players.
        """
        moved = False
        while not moved:
            x = random.randint(-self.size + 1, self.size - 1)
            max_y = self.size - abs(x) - 1
            y = random.randint(0, max_y)
            if (x,y) not in moves:
                moves.append((x, y))
                self.make_move(x,y)
                moved = True
        return moves

    def reset_game(self):
        """
        Reset the game to the initial state.
        """
        self.board = self._initialize_board()
        self.next_player_index = 0
        self.corner_claims = {player: set() for player in self.players}
        self.moves_made = 0

    def fill_moves_in_dict(self,moves):
        hex_board = [
            ['0'] * 1,  # x = -5
            ['0'] * 2,  # x = -4
            ['0'] * 3,  # x = -3
            ['0'] * 4,  # x = -2
            ['0'] * 5,  # x = -1
            ['0'] * 6,  # x = 0
            ['0'] * 5,  # x = 1
            ['0'] * 4,  # x = 2
            ['0'] * 3,  # x = 3
            ['0'] * 2,  # x = 4
            ['0'] * 1   # x = 5
        ]
        player_turn = [1, 2, 3]
        for idx, move in enumerate(moves):
            x, y = move
            adjusted_x = x + 5  
            if 0 <= adjusted_x < len(hex_board) and 0 <= y < len(hex_board[adjusted_x]):
                hex_board[adjusted_x][y] = str(player_turn[(idx) % 3])  
        return hex_board

    def find_next_board(self,moves):
        hex_board = self.fill_moves_in_dict(moves)
        zero_positions = [
            (row_idx, col_idx)
            for row_idx, row in enumerate(hex_board)
            for col_idx, value in enumerate(row)
            if value == '0'
        ]

        all_boards = []

        for row_idx, col_idx in zero_positions:
            new_board = [row[:] for row in hex_board]
            new_board[row_idx][col_idx] = '1'
            new_board_str = ''.join([''.join(row) for row in new_board])
            all_boards.append(new_board_str)
        return all_boards
    
    def find_corrdinates(self,index):
        list_length = [1,2,3,4,5,6,5,4,3,2,1]
        total = 0
        index = index - 1
        for row, length in enumerate(list_length):
            if total + length > index:
                col = index - total 
                return row-5,col
            total += length 
    def find_different_index(self,str1, str2):
        if len(str1) != len(str2):
            raise ValueError("String length should be same")
        
        diff_indices = [i for i in range(len(str1)) if str1[i] != str2[i]]
        
        if len(diff_indices) != 1:
            raise ValueError("more than 1 postion is different")
        
        return diff_indices[0]+1
    def ai_make_move(self,current_board,moves):
        board_key =  ''.join([''.join(row) for row in current_board])
        move_keys = list(matchbox_sets[board_key].keys())
        weights = list(matchbox_sets[board_key].values())
        selected_key = random.choices(move_keys, weights=weights, k=1)[0]
        move_number = self.find_different_index(board_key,selected_key)
        x,y = self.find_corrdinates(move_number)
        moves.append((x,y))
        return(selected_key), x, y
    
    def change_matchbox(self,ai_record,win_status):
        if win_status == "win":
            change = WIN
        elif win_status == "lose":
            change = LOSE
        elif win_status == "draw":
            change = LOSE    
        for record_list in ai_record:
            matchbox_sets[record_list[0]][record_list[1]] += change
            if matchbox_sets[record_list[0]][record_list[1]] == 0:
                matchbox_sets[record_list[0]][record_list[1]] = 1
        

    def new_game(self):
        self.reset_game()
        moves = []
        ai_record = []
        # Assuming that our ai player always go first to simplify the problem.
        for move_number in range(1,37):
            # This is ai player's turn
           
            # print(move_number)
            if (move_number %3) == 1:
                current_board = self.fill_moves_in_dict(moves)
                current_board_str = ''.join([''.join(row) for row in current_board])
                all_boards = self.find_next_board(moves)
                if current_board_str not in matchbox_sets:
                    matchbox_sets[current_board_str] = {item:1 for item in all_boards}
                
                ai_move_str,x,y = self.ai_make_move(current_board,moves)
                ai_record.append([current_board_str,ai_move_str])
                self.make_move(x,y)
                # print(matchbox_sets)
                # print(self.ai_make_move(current_board,moves))
                # print(moves)
                # print("this is ai turn:", move_number)
            #other two players turn.
            if (move_number % 3) != 1:
                # print("this is other two turn,",move_number)
                self.generate_random_1move(moves)
        self.check_corner_claims()
        if self.check_game_result() == "Red":
            status = "win"
        else:
            status = "lose"
        self.change_matchbox(ai_record,status)
            
        # print(ai_record)
        # print(matchbox_sets)
        return status
    def new_game_updated(self):
        self.reset_game()
        moves = []
        ai_record = []
        # Assuming that our ai player always go first to simplify the problem.
        for move_number in range(1,37):
            # This is ai player's turn
           
            # print(move_number)
            if (move_number %3) == 1:
                current_board = self.fill_moves_in_dict(moves)
                current_board_str = ''.join([''.join(row) for row in current_board])
                all_boards = self.find_next_board(moves)
                if current_board_str not in matchbox_sets:
                    matchbox_sets[current_board_str] = {item:1 for item in all_boards}
                
                ai_move_str,x,y = self.ai_make_move(current_board,moves)
                ai_record.append([current_board_str,ai_move_str])
                self.make_move(x,y)
                # print(matchbox_sets)
                # print(self.ai_make_move(current_board,moves))
                # print(moves)
                # print("this is ai turn:", move_number)
            #other two players turn.
            if (move_number % 3) != 1:
                # print("this is other two turn,",move_number)
                self.generate_random_1move(moves)
        self.check_corner_claims()
        if self.check_game_result_updated() == "Red":
            status = "win"
        elif self.check_game_result_updated() == "Draw":
            status = "draw"
        else:
            status = "lose"
        self.change_matchbox(ai_record,status)
            
        # print(ai_record)
        # print(matchbox_sets)
        return status
    def learn_games(self, game_number):
        total_win = 0
        total_other = 0
        win_rate_history = []

        for i in range(game_number):
            status = self.new_game()
            if status == "win":
                total_win += 1
            else:
                total_other += 1

            current_win_rate = total_win / (total_win + total_other)
            win_rate_history.append(current_win_rate)

        self.plot_win_rate(win_rate_history)

    def learn_games_updated(self, game_number):
        total_win = 0
        total_other = 0
        win_rate_history = []

        for i in range(game_number):
            status = self.new_game_updated()
            if status == "win":
                total_win += 1
            else:
                total_other += 1

            current_win_rate = total_win / (total_win + total_other)
            win_rate_history.append(current_win_rate)

        self.plot_win_rate(win_rate_history)


    def plot_win_rate(self,win_rate_history):
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(win_rate_history) + 1), win_rate_history, marker='o', linestyle='-', label='Win Rate')
        plt.xlabel("Game Number")  
        plt.ylabel("Win Rate")     
        plt.title("Win Rate Progression Over Games") 
        plt.legend()              
        plt.grid()                 
        plt.show()


if __name__ == '__main__':
    x_game = XGame(size=6)
    # moves = x_game.generate_random_moves(30)
    # print("Random moves:")
    # x_game.make_moves(moves)
    # x_game.check_game_result()
    # print(moves)
    # x_game.fill_moves_in_dict(moves)
    # x_game.find_next_board(moves)
    # print(len(x_game.find_next_board(moves)))
    # x_game.new_game()
    # x_game.display_board()
    # x_game.check_ending_value()
    # x_game.check_game_result()
    # print(x_game.corner_claims)
    # x_game.check_game_result_updated()
    x_game.learn_games_updated(1000000)

