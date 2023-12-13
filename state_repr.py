import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from params import *


class State_Repr(nn.Module):
    def __init__(self):
        super().__init__()
        self.user_embedding = nn.Embedding(user_num + 1, params['embedding_dim'])  # userid从1开始
        self.item_embedding = nn.Embedding(item_num + 1, params['embedding_dim'], padding_idx=0)  # movieid从1开始，初始用0填充

        self.ave = nn.Conv1d(in_channels=params['N'], out_channels=1, kernel_size=1)

        self.initialize()

    def initialize(self):
        nn.init.uniform_(self.ave.weight)
        self.ave.bias.detach().zero_()

    def forward(self, user, memory):
        user_embedding = self.user_embedding(user.long())
        item_embeddings = self.item_embedding(memory.long())
        # ave = self.ave(item_embeddings).squeeze(1)

        mean = torch.mean(item_embeddings, dim=1)

        return torch.cat([mean, mean*user_embedding, user_embedding], dim=1)
        # return torch.cat([ave, user_embedding * ave, user_embedding], dim=1)




