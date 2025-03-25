# train.py
import torch
import torch.nn as nn
from model import SimpleModel  # model.py에서 불러오기

# 데이터셋
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

# 모델, 손실함수, 옵티마이저
model = SimpleModel()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 학습 루프
for epoch in range(100):
    optimizer.zero_grad()
    output = model(X)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()

print("최종 손실:", loss.item())

# 모델 저장
torch.save(model.state_dict(), "model.pt")
