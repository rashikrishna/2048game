class Game2048:
    '''a 2048 game'''
    def __init__(self) -> None:
        import numpy as np
        from queue import Queue
        self.board = np.array([[0]*4 for _ in range(4)])
        self.empty = list((a, b) for a in range(4) for b in range(4))

    def _insert_element(self):
        '''Inserts a '2' tile in a random empty place'''
        from random import choice
        new_idx = choice(self.empty)
        self._update_empty_tiles()
        # self.empty.remove(new_idx)
        self.board[new_idx[0]][new_idx[1]] = 2

    def display_board(self):
        '''Prints out the board to the console'''
        for row in self.board:
            print(*row)
        print('-'*8)

    def _check_move(self, direction):
        '''Returns what board will be if a certain move is performed
        
        Parameters
        ----------
        direction: string
            direction to move
            
        Returns
        -------
        out: ndarray
            the board after performing the move'''
        import copy
        board_copy = copy.deepcopy(self.board)
        if direction == 'up' or direction == 'left':
            loop_params = (4, )
        elif direction == 'down' or direction == 'right':
            loop_params = (3, -1, -1)
        
        for col_idx in range(4):
            new_col = []
            # new_col_queue = Queue()
            for row_idx in range(*loop_params):
                if direction == 'up' or direction == 'down':
                    cell = board_copy[row_idx, col_idx]
                else:
                    cell = board_copy[col_idx, row_idx]
                if cell != 0:
                    try:
                        if cell == new_col[-1]:
                            new_col.pop()
                            new_col.append(cell*2)
                        else:
                            new_col.append(cell)
                    except IndexError:
                        new_col.append(cell)
            new_col.extend((0, 0, 0, 0))
            for idx, row_idx in enumerate(range(*loop_params)):
                if direction == 'up' or direction == 'down':
                    board_copy[row_idx, col_idx] = new_col[idx]
                else:
                    board_copy[col_idx, row_idx] = new_col[idx]
        return board_copy
    
    def check_if_won(self):
        '''Checks if any of the tile is 2048
        
        Returns
        -------
        out: bool
            True if any cell is 2048'''
        for row_idx, row in enumerate(self.board):
            for col_idx, cell in enumerate(row):
                if cell == 2048:
                    return True

    def _update_empty_tiles(self):
        self.empty = tuple((a,b) for a, row in enumerate(self.board) for b, cell in enumerate(row) if cell == 0)

    def perform_move(self, direction):
        '''Performs a move in a certain direction
        
        Parameters
        ----------
        direction: string
            direction to move
        '''
        new_board = self._check_move(direction)
        if (new_board != self.board).any():
            self.board = new_board
            self._update_empty_tiles()

    def is_game_over(self):
        '''Checks if the game is over
        
        Returns
        -------
        out: bool
            returns True if game is over'''
        all_moves = ['up', 'down', 'left', 'right']
        for move in all_moves:
            if (self._check_move(move) != self.board).any():
                return False
        return True

if __name__ == '__main__':
    game = Game2048()
    # print(game.board)
    # print(game.empty)
    game.display_board()
    game._insert_element()
    game.display_board()
    game._insert_element()
    game.display_board()
    game._insert_element()
    game.display_board()
    # game._insert_element()
    game.perform_move('right')
    game.display_board()
    game.update_empty_tiles()
    print(game.empty)
    game.perform_move('left')
    game.display_board()
    game.update_empty_tiles()
    print(game.empty)

