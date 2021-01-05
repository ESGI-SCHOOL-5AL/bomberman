import arcade
import random
import numpy as np
from sklearn.neural_network import MLPRegressor

from datetime import datetime

from .policy import Policy
from .actions import *

from ..game.player import Player
from ..game.bomb import Bomb
from ..game.bomb import Explosion

TILES = {
    "Floor": 0 / 5,
    "Wall": 1 / 5,
    "Brick": 2 / 5,
    "Bomb": 3 / 5,
    "Explosion": 4 / 5,
    "Agent": 5 / 5
}

REWARD_IMPOSSIBLE = -100
REWARD_DEATH = -100
REWARD_DEFAULT = 5
REWARD_IDLE = -1
REWARD_MOVE_NEAR_BOMB = -1
REWARD_BOMB = 20
REWARD_DESTROY_BRICKS = 30
REWARD_KILL = 40
REWARD_WIN = 60


class Agent(Player):

    def __init__(self, environment, policy=None):
        super().__init__(environment)
        if policy == None:
            policy = Policy(ACTIONS)
        self.policy = policy
        self.reset()

    def reset(self):
        super().reset()
        self.score = 0
        self.previous_state = self.makeState()

    def makeState(self):
        # TODO add players too
        states = [[]]

        for line in self.environment.grid:
            for element in line:
                states[0].append(TILES[element.__class__.__name__])

        states[0].append(self.x / 15)
        states[0].append(self.y / 15)

        return states

    def update(self, delta_time):
        if not self.alive:
            return

        state = self.makeState()
        self.previous_state = state
        reward = REWARD_DEFAULT
        action = self.policy.choose_action(state)
        bomb_count = self.current_bombs

        # there is a bomb at player's location
        is_bomb = isinstance(self.environment.grid[self.y][self.x], Bomb)

        if action != IDLE:
            self.move(action, 0)
            state = self.makeState()
        else:
            reward = REWARD_IDLE

        if self.previous_state[0] == self.x and self.previous_state[1] == self.y and action != BOMB and action != IDLE:
            reward = REWARD_IMPOSSIBLE
        elif action == BOMB:
            if is_bomb or bomb_count >= self.max_bombs:
                reward = REWARD_IMPOSSIBLE
            else:
                reward = REWARD_BOMB
        elif isinstance(self.environment.grid[self.y][self.x], Explosion) and action != BOMB and action != IDLE:
            reward = REWARD_DEATH
        elif not is_bomb and action != BOMB and action != IDLE and self.nearBomb():
            reward = REWARD_MOVE_NEAR_BOMB

        self.score += reward
        self.policy.update(self.previous_state, state, action, reward)

    def nearBomb(self):
        return isinstance(self.environment.grid[self.y-1][self.x], Bomb) or \
            isinstance(self.environment.grid[self.y+1][self.x], Bomb) or \
            isinstance(self.environment.grid[self.y][self.x-1], Bomb) or \
            isinstance(self.environment.grid[self.y][self.x+1], Bomb)

    def onWin(self):
        self.score += REWARD_WIN
        self.policy.update(self.previous_state,
                           self.makeState(), IDLE, REWARD_WIN)

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
        self.policy.update(self.previous_state, self.makeState(), BOMB, reward)
