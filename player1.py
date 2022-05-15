from gameboard import Board
import socket
import json
'''Player 1 will ask the user for the host information of player 2:
Prompt the user for the host name/IP address of player 2 they want to play with
Prompt the user for the port to use in order to play with player 2
Using that information they will attempt to connect to player 2
Upon successful connection they will send player 2 the their user name (over the socket, just alphanumeric user name with no special characters)
If the connection cannot be made then the user will be asked if they want to try again:
If the user enters 'y' then you will request the host information from the user again
If the user enters 'n' then you will end the program
Once player 1 receives player 2's username or if the users decides to play again (see step 4.2 below)
Player 1 will ask the user for their move using the built-in input() function
and send it to player 2.
Player 1 will always be x/X
Player 1 will always send the first move to player 2
Each move will correspond to the input given using the keyboard.
Once player 1 sends their move they will wait for player 2's move.
Repeat steps 3.1.2 - 3.1.4 until the game is over (A game is over when a winner is found or the board is full)
Once a game as finished (win or tie) the user will indicate if they want to play again using the command line.
If the user enters 'y' or 'Y' then player 1 will send "Play Again" to player 2
If the user enters 'n' or 'N' then player 1 will send "Fun Times" to player 2 and end the program
Once the user is done player they will print all the statistics.'''


class player1:
    def __init__(self, name: str):
        self.name = name
        self.letter = 'X'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip: str = 'localhost', port: int = 12345) -> bool:
        '''
        attempts to connect to player 2
        sends username to p2
        waits $timeout seconds for a response
            if none, raise exception
        else, create board game with p1 and p2
        '''
        try:
            self.sock.connect((ip, port))
        except ConnectionRefusedError as e:
            return e

        try:
            self.sock.send(json.dumps(
                {'type': 'name', 'data': self.name}).encode())
            incoming = json.loads(self.sock.recv(1024).decode())
            if incoming['type'] != 'name':
                raise ValueError('A name waas not recieved')

            self.opponentName = incoming['data']

            print(self.opponentName)

            self.board = Board(self.name, self.OpponentName,
                               lastTurn=self.OpponentName)

        except Exception as e:
            return e

    def move(self, pos: tuple, letter=None):
        '''
        makes a move and sends move to p2 over socket
        '''
        letter = self.letter if letter is None else letter

        self.board.updateGameBoard(pos, self.letter)
        self.sock.send(self.sock.send(json.dumps(
            {'type': 'move', 'data': {'pos': pos, 'letter': self.letter}}).encode()))

    def recvMove(self):
        incoming = json.laods(self.sock.recv(1024).decode())

        if incoming['type'] != 'move':
            raise ValueError('type of message received is not a move')

        self.board.updateGameBoard(
            incoming['data']['pos'], incoming['data']['letter'])

    def close(self):
        '''
        clean up socekt
        '''

        self.sock.close()

    def getBoard(self) -> str:
        return self.board.getBoard()


def playGame(player: player1) -> None:
    while not player.board.boardIsFull:
        moveComp = False
        while not moveComp:
            try:
                input()
                player.move()


def main():
    name = input('what is your name?')
    ipAddr = int('what is the ip address of the other user?')
    port = int('what is the port?')

    player = player1(name)

    connected = False
    while not connected:
        try:
            player.connect(ipAddr, port)
        except Exception as e:
            print(e)
            tryAgain = input(
                'connection failed, would you like to try again? (Y or N').lower()
            if tryAgain == 'y':
                continue
            if tryAgain == 'n':
                break
            else:
                print('invalid input recieved')

    if connected == True:
        print(f'starting new game with {player.opponentName}')

        playing = True
        while playing():
            play_game()
            inputRec = False
            while not inputRec:
                playAgain = input(
                    'would you like to play again (Y or N').lower()
                if playAgain == 'y':
                    inputRec = True
                elif playAgain == 'n':
                    playing = False
                    player.close()
                else:
                    print('Invalid input recieved')

    print('goodbye')


if __name__ == '__main__':
    main()
