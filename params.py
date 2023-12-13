import torch

# 把所有超参定义在这
params = {
    'embedding_dim': 72,
    'hidden_dim': 72,
    'N': 5,  # 状态中物品数量
    'ou_noise': False,
    'critic_lr': 1e-5,
    'critic_decay': 1e-4,
    'actor_lr': 1e-5,
    'actor_decay': 1e-6,
    'state_repr_lr': 1e-5,
    'state_repr_decay': 1e-3,
    'gamma': 0.8,
    'min_value': -10,
    'max_value': 10,
    'soft_tau': 1e-3,
    'sigma': 0.01,
    'buffer_capacity': 1000000,
    'batch_size': 64,
    'minimal_size': 1000,
    'max_episode_num': 10000  # 训练轮次
}

# 用户以及电影数量
user_num = 6040
item_num = 3952

# 测试频率
eval_frequency = 500

# 测试时候推荐list长度
top_ks = [5, 10]


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
