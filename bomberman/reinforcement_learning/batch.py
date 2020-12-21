import numpy as np
from sklearn.neural_network import MLPRegressor

class Batch:
    def __init__(self, batch_size):
        self.inputs = []
        self.outputs = []
        self.batch_size = batch_size
        self.batch_iteration = 0

    def reset(self):
        self.inputs = []
        self.outputs = []
        self.batch_size = 0

    def update_batch(self, inputs, outputs):
        if self.batch_iteration == self.batch_size:
            return (self.inputs, self.outputs)

        self.batch_iteration += 1
        self.inputs.append(inputs)
        self.outputs.append(outputs)

        return None
