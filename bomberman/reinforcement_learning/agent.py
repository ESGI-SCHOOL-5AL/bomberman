import arcade

from ..game.player import Player
from ..game.bomb import Bomb
from ..game.bomb import Explosion

MOVE_UP = arcade.key.Z
MOVE_LEFT = arcade.key.Q
MOVE_DOWN = arcade.key.S
MOVE_RIGHT = arcade.key.D
BOMB = arcade.key.SPACE
IDLE = 0
ACTIONS = [MOVE_UP, MOVE_DOWN,
           MOVE_LEFT, MOVE_RIGHT, BOMB, IDLE]

REWARD_IMPOSSIBLE = -100
REWARD_DEATH = -60
REWARD_DEFAULT = -1
REWARD_IDLE = -2
REWARD_MOVE_NEAR_BOMB = -10
REWARD_BOMB = 30
REWARD_DESTROY_BRICKS = 20
REWARD_KILL = 40
REWARD_WIN = 60

DEFAULT_LEARNING_RATE = 0.1
DEFAULT_DISCOUNT_FACTOR = 0.8


class Agent(Player):

    def __init__(self, environment, policy=None):
        super().__init__(environment)
        if policy == None:
            policy = Policy(environment.generateStates(), ACTIONS)
        self.policy = policy
        self.reset()

    def reset(self):
        super().reset()
        self.score = 0
        self.previous_state = self.makeState()

    def makeState(self):
        #  OOO
        #  OXO
        #  OOO
        # Square representing agent's vision
        # TODO add players too
        return (
            self.environment.grid[self.y-1][self.x-1].__class__.__name__,
            self.environment.grid[self.y-1][self.x].__class__.__name__,
            self.environment.grid[self.y-1][self.x+1].__class__.__name__,
            self.environment.grid[self.y][self.x-1].__class__.__name__,
            self.environment.grid[self.y][self.x].__class__.__name__,
            self.environment.grid[self.y][self.x+1].__class__.__name__,
            self.environment.grid[self.y+1][self.x-1].__class__.__name__,
            self.environment.grid[self.y+1][self.x].__class__.__name__,
            self.environment.grid[self.y+1][self.x+1].__class__.__name__,
        )

    def update(self, delta_time):
        if not self.alive:
            return

        state = self.makeState()
        reward = REWARD_DEFAULT
        action = self.policy.best_action(state)
        self.previous_state = state

        # there is a bomb at player's location
        is_bomb = isinstance(self.environment.grid[self.y][self.x], Bomb)

        if action != IDLE:
            self.move(action, 0)
        else:
            reward = REWARD_IDLE

        if self.previous_state[0] == self.x and self.previous_state[1] == self.y and action != BOMB and action != IDLE:
            reward = REWARD_IMPOSSIBLE
        elif action == BOMB and self.current_bombs >= self.max_bombs:
            reward = REWARD_IMPOSSIBLE
        elif action == BOMB and (self.current_bombs >= self.max_bombs or is_bomb):
            reward = REWARD_IDLE
        elif action == BOMB and not is_bomb:
            reward = REWARD_BOMB
        elif isinstance(self.environment.grid[self.y][self.x], Explosion) and action != BOMB and action != IDLE:
            reward = REWARD_DEATH
        elif action != BOMB and action != IDLE and self.nearBomb():
            reward = REWARD_MOVE_NEAR_BOMB

        self.score += reward
        self.policy.update(self.previous_state, state, action, reward)

    def nearBomb(self):
        return isinstance(self.environment.grid[self.y-1][self.x], Bomb) or \
            isinstance(self.environment.grid[self.y+1][self.x], Bomb) or \
            isinstance(self.environment.grid[self.y][self.x-1], Bomb) or \
            isinstance(self.environment.grid[self.y][self.x+1], Bomb)

    def onDeath(self):
        super().onDeath()
        # reward = REWARD_DEATH
        # self.score += reward
        # -1 means he is not responsible
        # self.policy.update(self.previous_state, self.makeState(), -1, reward)

    def onKill(self, player):
        reward = REWARD_KILL
        if player == self:
            reward *= -1
        self.score += reward
        # TODO how to match source action?
        # self.policy.update(self.previous_state, self.makeState(), BOMB, reward)

    def onDestroyBrick(self, brick):
        reward = REWARD_DESTROY_BRICKS
        self.score += reward
        # self.policy.update(self.previous_state, self.makeState(), BOMB, reward)


class Policy:  # Q-table
    def __init__(self, states, actions,
                 learning_rate=DEFAULT_LEARNING_RATE,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR):
        self.table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        for s in states:
            self.table[s] = {}
            for a in actions:
                self.table[s][a] = 0

    def __repr__(self):
        res = ''
        for state in self.table:
            res += f'{state}\t{self.table[state]}\n'
        return res

    def best_action(self, state):
        action = None
        for a in self.table[state]:
            if action is None or self.table[state][a] > self.table[state][action]:
                action = a
        return action

    def update(self, previous_state, state, last_action, reward):
        if last_action == -1:
            # TODO should update policy on death (action == -1)
            return
        # Q(st, at) = Q(st, at) + learning_rate * (reward + discount_factor * max(Q(state)) - Q(st, at))
        maxQ = max(self.table[state].values())
        self.table[previous_state][last_action] += self.learning_rate * \
            (reward + self.discount_factor * maxQ -
             self.table[previous_state][last_action])
