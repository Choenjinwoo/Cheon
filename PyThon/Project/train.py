# train.py
import torch
import torch.nn as nn
from model import SimpleModel

# 학습용 더미 데이터
X = torch.tensor([
    [25, 36.5, 120],
    [45, 38.1, 140],
    [30, 37.0, 130]
], dtype=torch.float32)

y = torch.tensor([
    [0.1],
    [0.9],
    [0.3]
], dtype=torch.float32)

model = SimpleModel()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(300):
    optimizer.zero_grad()
    output = model(X)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()

print("최종 손실:", loss.item())

torch.save(model.state_dict(), "model.pt")
