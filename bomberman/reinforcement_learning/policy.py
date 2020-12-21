import numpy as np
from sklearn.neural_network import MLPRegressor

from .actions import *

DEFAULT_LEARNING_RATE = 0.003
DEFAULT_DISCOUNT_FACTOR = 0.8

class Policy:  # MLPRegressor
    def __init__(self, actions,
                 learning_rate=DEFAULT_LEARNING_RATE,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.actions = actions
        self.mlp = MLPRegressor(hidden_layer_sizes = (10,),
                                activation = 'tanh',
                                solver = 'sgd',
                                learning_rate_init = self.learning_rate,
                                max_iter = 1,
                                alpha=0.5,
                                warm_start = True)
        self.mlp.fit([[
            0, 0, 0,
            0, 0, 0,
            0, 0, 0, 0
            ]],
            [[0, 0, 0, 0, 0, 0]]
        )
        self.q_vector = None

    def __repr__(self):
        return self.q_vector

    def best_action(self, state):
        self.q_vector = self.mlp.predict(np.array(state))[0]
        action = self.actions[np.argmax(self.q_vector)]
        return action

    def update(self, previous_state, state, last_action, reward):
        maxQ = np.amax(self.q_vector)
        last_action = ACTIONS.index(last_action)
        self.q_vector[last_action] = reward + self.discount_factor * maxQ

        inputs = np.array(previous_state)
        outputs = np.array([self.q_vector])
        print(inputs, outputs)
        self.mlp.fit(inputs, outputs)
        
        # MLPRegressor(hidden_layer_sizes = (10,),
        #                         activation = 'tanh',
        #                         solver = 'sgd',
        #                         learning_rate_init = self.learning_rate,
        #                         max_iter = 1,
        #                         alpha=0.5,
        #                         warm_start = True).fit(inputs, outputs)
