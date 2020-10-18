import arcade

from ..game.player import Player
from ..game.bomb import Bomb

ACTIONS = [arcade.key.Z, arcade.key.S, arcade.key.Q, arcade.key.D, arcade.key.SPACE, 0]

REWARD_IMPOSSIBLE = -60
REWARD_DEATH = -50
REWARD_DEFAULT = -2
REWARD_IDLE = -1
REWARD_BOMB = -40
REWARD_DESTROY_BRICKS = 5
REWARD_KILL = 60
REWARD_WIN = 80

DEFAULT_LEARNING_RATE = 1
DEFAULT_DISCOUNT_FACTOR = 0.5

# TODO position relatve des autres joueurs, position des bombes

class Agent(Player):

    def __init__(self, environment):
        super().__init__(environment)
        self.policy = Policy(environment.states.keys(), ACTIONS)
        self.reset()

    def reset(self):
        super().reset()
        self.score = 0
        self.last_action = 0
        self.previous_state = (self.x, self.y)

    def update(self, delta_time):
        if not self.alive:
            return

        state = (self.x, self.y)
        reward = REWARD_DEFAULT
        action = self.policy.best_action(state)
        self.previous_state = state
        is_bomb = isinstance(self.environment.grid[self.y][self.x], Bomb) # there is a bomb at player's location
        if action != 0: # 0 means do nothing
            self.move(action, 0)
            reward = REWARD_IDLE


        if self.previous_state[0] == self.x and self.previous_state[1] == self.y and action != arcade.key.SPACE and action != 0:
            reward = REWARD_IMPOSSIBLE
        elif action == arcade.key.SPACE and not is_bomb:
            reward = REWARD_BOMB
        
        self.score += reward
        self.policy.update(self.previous_state, state, action, reward)
        print(self.score)

    def onDeath(self):
        super().onDeath()
        reward = REWARD_DEATH
        self.score += reward
        self.policy.update(self.previous_state, (self.x, self.y), -1, reward) # -1 means he is not responsible

    def onKill(self, player):
        reward = REWARD_KILL
        self.score += reward
        self.policy.update(self.previous_state, (self.x, self.y), -1, reward) # TODO how to match source action?
    
    def onDestroyBrick(self, brick):
        reward = REWARD_DESTROY_BRICKS
        self.score += reward
        self.policy.update(self.previous_state, (self.x, self.y), -1, reward)

class Policy: #Q-table
    def __init__(self, states, actions,
                 learning_rate = DEFAULT_LEARNING_RATE,
                 discount_factor = DEFAULT_DISCOUNT_FACTOR):
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
            return # TODO should update policy on death (action == -1), on brick destroyed
        #Q(st, at) = Q(st, at) + learning_rate * (reward + discount_factor * max(Q(state)) - Q(st, at))
        maxQ = max(self.table[state].values())
        self.table[previous_state][last_action] += self.learning_rate * \
            (reward + self.discount_factor * maxQ - self.table[previous_state][last_action])