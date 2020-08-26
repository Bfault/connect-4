class Game:
    '''
        Manage all the game settings
    '''
    def __init__(self, weight=7, height=6):
        self.weight = weight
        self.height = height
        self.board = self._set_board()
    
    def _set_board(self):
        '''
            set space in tab
        '''
        output = []
        for y in range(self.height):
            output.append([])
            for x in range(self.weight):
                output[y].append(' ')
        return output
    
    def get_state(self):
        '''
            return if game is over or not
        '''
        if 1 == 0:
            return 0
        return 1

    def action(self, token, column):
        '''
            refresh game with player turn
        '''
        pass

    def display(self):
        '''
            show the progress of the game
        '''
        for y in range(self.height):
            print('#', end='')
            for x in range(self.weight):
                print(self.board[y][x], end='')
            print('#')
        print('#'*(self.weight + 2))

class Player:
    '''
        manage player movements
    '''
    def __init__(self):
        self.name = self._get_name()
        self.token = self._get_token()

    def _get_name(self):
        name = input("Choose your name : ")
        if len(name) == 0:
            name = self._get_name()
        return name

    def _get_token(self):
        token = input("Choose your token shape : ")
        if len(token) != 1:
            token = self._get_token()
        return token
    
    def _validate_column(self, column):
        return 1

    def turn(self):
        '''
            get input to make player's turn
        '''
        column = input("{name} playing, which column ? (1-{end}) -> ".format(name=self.name, end=game.weight))
        if not self._validate_column(column):
            return self.turn()
        return self.token, column

if __name__ == '__main__':
    game = Game()
    p1 = Player()
    p2 = Player()
    players = [p1, p2]
    o = 0

    while game.get_state():
        print()
        game.display()
        game.action(players[o].turn())
        o = -o + 1