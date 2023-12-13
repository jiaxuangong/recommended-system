import torch
import numpy as np
import torch.nn as nn
from params import *


class Critic(nn.Module):
    def __init__(self):
        super().__init__()

        self.layers = nn.Sequential(
            nn.Linear(params['embedding_dim'] * 4, params['hidden_dim']),
            # nn.Linear(params['embedding_dim'] * 2, params['hidden_dim']),#这是没用userid的时候
            nn.ReLU(),
            nn.Linear(params['hidden_dim'], params['hidden_dim']),
            nn.ReLU(),
            nn.Linear(params['hidden_dim'], 1)
        )

        self.initialize()

    def initialize(self):
        for l in self.layers:
            if isinstance(l, nn.Linear):
                nn.init.kaiming_uniform_(l.weight)
                nn.init.uniform_(l.bias)

    def forward(self, state_embedding, action_embedding):
        x = torch.cat([state_embedding, action_embedding], dim=1)
        return self.layers(x)


