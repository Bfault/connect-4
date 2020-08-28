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
    
    def _check_right(self, pos, token, power):
        x, y = pos
        if x + 1 >= self.weight or self.board[y][x + 1] != token or power == 4:
            return power
        else:
            return self._check_right((x + 1, y), token, power + 1)

    def _check_left(self, pos, token, power):
        x, y = pos
        if x - 1 < 0 or self.board[y][x - 1] != token or power == 4:
            return power
        else:
            return self._check_left((x - 1, y), token, power + 1)

    def _check_top(self, pos, token, power):
        x, y = pos
        if y + 1 >= self.height or self.board[y + 1][x] != token or power == 4:
            return power
        else:
            return self._check_top((x, y + 1), token, power + 1)

    def _check_bot(self, pos, token, power):
        x, y = pos
        if y - 1 < 0 or self.board[y - 1][x] != token or power == 4:
            return power
        else:
            return self._check_bot((x, y - 1), token, power + 1)

    def _fill_state(self, token):
        '''
            fill state for bots
        '''
        state = []
        for y, _ in enumerate(self.board):
            state.append([])
            for case in self.board[y]:
                if case == token:
                    state[y].append(1)
                elif case == ' ':
                    state[y].append(0)
                else:
                    state[y].append(-1)
        return state


    def get_state(self, pos, token):
        '''
            return if game is over or not
        '''
        state = self._fill_state(token)

        if token == ' ' or pos == (-1, -1):
            return 1, state
        
        check_around = [
            self._check_bot(pos, token, 1),
            self._check_top(pos, token, 1),
            self._check_left(pos, token, 1),
            self._check_right(pos, token, 1)
        ]

        for checking in check_around:
            if checking >= 4:
                return 0, state
        return 1, state

    def _get_reward(self, pos, token):
        '''
            compute reward for given choice
        '''
        reward = 0
        x, y = pos
        check_around = [
            self._check_bot(pos, token, 1),
            self._check_top(pos, token, 1),
            self._check_left(pos, token, 1),
            self._check_right(pos, token, 1)
        ]

        for checking in check_around:
            reward += checking
        
        return reward - 4

    def action(self, token, column):
        '''
            refresh game with player turn
        '''
        for y, place in reversed(list(enumerate(self.board))):
            if place[column] == ' ':
                place[column] = token
                reward = self._get_reward((column, y), token)
                return (column, y), reward

    def display(self):
        '''
            show the progress of the game
        '''
        print()
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
    token_lib = []
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
        if len(token) != 1 or any(token in s for s in Player.token_lib) or token == ' ':
            print("Token already taken or invalid (valid is one character except space")
            token = self._get_token()
        Player.token_lib.append(token)
        return token
    
    def _validate_column(self, column):
        if column < 1 or column > game.weight:
            print("Out of range")
            return 0
        if game.board[0][column - 1] != ' ':
            print("Already filled")
            return 0
        return 1

    def turn(self):
        '''
            get input to make player's turn
        '''
        column = int(input("{name} playing, which column ? (1-{end}) -> ".format(name=self.name, end=game.weight)))
        if not self._validate_column(column):
            return self.turn()
        return self.token, column - 1

if __name__ == '__main__':
    game = Game()
    p1 = Player()
    p2 = Player()
    players = [p1, p2]

    o = 1
    pos = (-1, -1)
    token = ' '
    status = 1

    while status:
        o = -o + 1
        game.display()
        token, column = players[o].turn()
        pos, reward = game.action(token, column)
        status, state = game.get_state(pos, token)
    game.display()
    print("\n{player} win this game, GG!!".format(player=players[o].name))