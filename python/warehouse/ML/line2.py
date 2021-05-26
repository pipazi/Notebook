# -*- coding: utf-8 -*-
"""
Created on 2021/5/11 11:44

@author: sun shaowen
"""
import torch
from sklearn.datasets import load_boston


class LinearModel(torch.nn.Module):
    def __init__(self, ndim):
        super(LinearModel, self).__init__()
        self.ndim = ndim
        self.weight = torch.nn.Parameter(torch.randn(ndim, 1))
        self.bias = torch.nn.Parameter(torch.rand(1))

    def forward(self, x):
        # y = Wx + b
        return x.mm(self.weight) + self.bias


lm = LinearModel(13)
criterion = torch.nn.MSELoss()
optim = torch.optim.SGD(lm.parameters(), lr=1e-6)

boston = load_boston()
data = torch.tensor(boston["data"], requires_grad=True, dtype=torch.float32)
target = torch.tensor(boston["target"], dtype=torch.float32)
print(data.size(), target.size())

for epoch in range(10000):
    # Forward pass
    predict = lm(data)
    loss = criterion(predict, target)

    # Backward and optimize
    optim.zero_grad()
    loss.backward()
    optim.step()

    if epoch and epoch % 1000 == 0:
        print(data.grad)
        print("[{} / 100000] Loss: {:.3f}".format(epoch, loss.item()))


print(lm.weight)
print(lm.bias)



