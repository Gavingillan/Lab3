from gameboard import Board
import socket
import json

'''The user will be asked to provide the host information so that it can establish a socket connection.
Player 2 will accept incoming requests to start  a new game
When a connection request is received and accepted, player 2 will wait for player 1 to send their user name
Once player 2 receives player 1's user name, then player 2 will send "player2" as their user name to player 1 (over the socket) and wait for player 1 to send their move.
Once player 2 receives player 1's move they will ask the user for their move and send it to player 1 using the built-in input() function.
Each move will correspond to the input given using the keyboard.
Once player 2 sends their move they will wait for player 1's move.
Repeat steps 3.1 - 3.2 until the game is over (A game is over when a winner is found or the board is full)
Once a game as finished (win or tie) player 2 will wait for player 1 to indicate if they want to play again using the command line.
If player 1 wants to play again then player 2 will wait for player 1's first move.
If player 1  does not wants to play again then player 2 will print the statistics'''


class player2:
    def __init__(self, name) -> None:
        self.name = name
        self.letter = 'O'

    def connect(self, ip: str = 'localhost', port: int = 12345) -> None:
        '''
        awaits connectiong from p1
        returns name
        creates new gameboard for use with p1
        '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))

        self.sock.listen(1)
        self.opponentSocket, _ = self.sock.accept()
        incoming = json.loads(self.opponentSocket.recv(1024).decode())

        # check if data recieved is a name
        if incoming['type'] != 'name':
            raise ValueError('A name waas not recieved')
        else:
            self.opponentName = incoming['data']

        self.opponentSocket.send(json.dumps(
            {'type': 'name', 'data': self.name}).encode())

        self.board = Board(self.opponentName, self.name, lastTurn=self.name)

    def move(self, pos: tuple, letter=None) -> None:
        '''
        Parameters: position(Tuple) (row,col)
        checks to see if postion is still open
        if it is, put an X or an O in the position
        '''
        letter = self.letter if letter is None else letter

        self.board.updateGameBoard(pos, letter)
        self.opponentSocket.send(self.sock.send(json.dumps(
            {'type': 'move', 'data': {'pos': pos, 'letter': self.letter}}).encode()))

    def close(self) -> None:
        '''
        clean up socket and shutdown gracefully
        '''


def main():
    # connect
    p2 = player2("anus")
    p2.connect()

    # play game

    # ask if wanna play again

    # quit


if __name__ == '__main__':
    main()
