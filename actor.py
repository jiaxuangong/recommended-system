import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from params import *


class Actor(nn.Module):
    def __init__(self):
        super().__init__()

        self.layers = nn.Sequential(
            nn.Linear(params['embedding_dim'], params['hidden_dim']),
            nn.Linear(params['hidden_dim'], params['hidden_dim']),
            nn.Linear(params['hidden_dim'], params['embedding_dim']),
        )


        self.initialize()

    def initialize(self):
        for l in self.layers:
            if isinstance(l, nn.Linear):
                nn.init.zeros_(l.bias.data)
                nn.init.eye_(l.weight.data)

    def forward(self, x):
        return self.layers(x[:,:params['embedding_dim']])



