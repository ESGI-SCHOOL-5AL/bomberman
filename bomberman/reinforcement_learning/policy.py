import numpy as np
import random
from sklearn.neural_network import MLPRegressor

from .actions import *
from .batch import Batch

DEFAULT_LEARNING_RATE = 0.003
DEFAULT_DISCOUNT_FACTOR = 0.8

class Policy:  # MLPRegressor
    def __init__(self, actions,
                 learning_rate=DEFAULT_LEARNING_RATE,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR):
        self.epsilon = 1
        self.final_epsilon = 0.01
        self.n_step = 10**6
        self.epsilon_step = (self.epsilon - self.final_epsilon) / self.n_step
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
        self.batch = Batch(32)

    def __repr__(self):
        return self.q_vector

    def choose_action(self, state):
        if random.random() < self.epsilon:
            # action = random.randrange(len(ACTIONS))
            action = random.choice(ACTIONS)
        else:
            action = self.best_action(state)

        self.epsilon = max(self.epsilon - self.epsilon_step, self.final_epsilon)
        return action

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

        batch_result = self.batch.update_batch(inputs, outputs)

        if batch_result:            
            self.mlp.fit(np.array(batch_result[0]).reshape(-1, len(inputs[0])), np.array(batch_result[1]).reshape(-1, len(outputs[0])))
            self.batch.reset()

        
