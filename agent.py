import numpy as np
import torch
import torch.nn as nn
from actor import Actor
from critic import Critic
from state_repr import State_Repr
from torch.optim import *
from params import *
import torch.nn.functional as F


class Agent:
    def __init__(self):
        self.actor = Actor()
        self.critic = Critic()
        self.state_repr = State_Repr()
    def get_action(self, user_id, liked_items, action_space, is_test=False, online=0):
        # 第0维度加一个batch_size维度，才可以输入到网络层中
        user_id = torch.tensor([user_id], dtype=torch.long).to(device)
        liked_items = torch.tensor([liked_items], dtype=torch.long).to(device)
        action_space = torch.tensor(list(action_space), dtype=torch.long).to(device)

        state_embed = self.state_repr(user_id, liked_items)
        action_embed = self.actor(state_embed)

        if not is_test:
            # 如果是处于训练阶段,加高斯噪声
            action_embed = action_embed + torch.randn_like(action_embed) * params['sigma']*2

        items_embeddings = self.state_repr.item_embedding(action_space)
        scores = torch.matmul(items_embeddings, action_embed.T)

        if not online:  # 训练和测试都是每次推荐一个
            action_index = torch.gather(action_space, 0, scores.argmax(0))
            return action_embed, action_index.item()
        else:  # 真正在线用了就一次推荐online个,online为0则指示为训练或者测试阶段，不为0说明是online并且表示topk
            top_k_scores, top_k_indices = torch.topk(scores, online, dim=0)
            top_k_indices = top_k_indices.squeeze()
            top_k_action_index = torch.index_select(action_space, 0, top_k_indices)
            return action_embed, top_k_action_index

    def soft_update(self, net: nn.Module, target_net: nn.Module):
        for param_target, param in zip(target_net.parameters(), net.parameters()):
            param_target.detach().copy_(
                param_target.detach() * (1 - params['soft_tau']) + param.detach() * params['soft_tau'])

    def save_model(self, actor_path, critic_path, state_repr_path):
        torch.save(self.actor.state_dict(), actor_path)
        torch.save(self.critic.state_dict(), critic_path)
        torch.save(self.state_repr.state_dict(), state_repr_path)

    def load_model(self, actor_path, critic_path, state_repr_path):
        self.actor.load_state_dict(torch.load(actor_path))
        self.critic.load_state_dict(torch.load(critic_path))
        self.state_repr.load_state_dict(torch.load(state_repr_path))
