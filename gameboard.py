from typing import Tuple


class Board:
    def __init__(self, wins=0, ties=0, losses=0, lastTurn=None):
        self.wins = wins
        self.ties = ties
        self.losses = losses
        self.lastTurn = lastTurn
        self.gamesPlayed = wins+ties+losses

        self.resetGameBoard()

    def updateGamesPlayed(self, num: int = 1) -> None:
        '''
        @param num (optional): the number to increment the number of games by;
            default is 1
        '''
        self.gamesPlayed += num

    def resetGameBoard(self):
        '''
        resets the game board to a 3x3 matrix with 1 white space
        '''
        self.board = [['', '', ''],
                      ['', '', ''],
                      ['', '', '']]

    def updateGameBoard(self, pos: tuple, player: str) -> None:
        '''
        adds an x if player 1 plays
        adds an o if player 2 plays
        at given position

        @param pos:tuple (row,col) to change to an X or an O

        @raises: ValueError if position is already taken

        @raises: ValueError if player is not X or O

        @raises: indexOutOfBoundsError if pos is outside of 3x3 matrix
        '''
        if player not in ['X', 'O']:
            raise ValueError('Invlaid player')

        if self.board[pos[0]][pos[1]] == '':
            raise ValueError('position is already taken')

    def isWinner(self, player: str) -> bool:
        '''
        checks if any row, col or diagonal of the board is full of the same character

        @param player:str of player to check if they win

        @return bool: if player won or not
        '''
        for row in self.board:
            if row[0] == row[1] == row[2] == player:
                return True

        for col in zip(self.board):
            if col[0] == col[1] == col[2] == player:
                return True

        for i in range(len(self.board)):
            if self.board[i][i] != player:
                return False
        return True

    def boardIsFull(self) -> bool:
        '''
        checks if board is full

        @return bool whether or not board is full
        '''
        for row in self.board:
            for item in row:
                if item == '':
                    return False
        return True

    def printStats(self) -> str:
        pass

    def getBoard(self) -> str:
        outStr = ''
        for row in self.board:
            for col in row:
                outStr += col
            outStr += '\n'
        return outStr
