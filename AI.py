import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.model_selection import train_test_split

# 1. 샘플 데이터 생성
X = np.random.rand(100, 5)  # 100개의 데이터, 각 데이터는 5개의 숫자로 구성
y = np.random.randint(0, 2, size=(100,))  # 0 또는 1 예측 (분류 문제)

# 데이터를 PyTorch 텐서로 변환
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_test = torch.tensor(X_train, dtype=torch.float32), torch.tensor(X_test, dtype=torch.float32)
y_train, y_test = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1), torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

#2. MLP 모델 정의
class MLP(nn.Module):
    def __init__(self, input_size, output_size):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 64)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(64, output_size)
        self.sigmoid = nn.Sigmoid()  # 출력값을 0~1로 변환

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return self.sigmoid(x)  # 분류 문제이므로 sigmoid 사용

#3. 모델 생성
model = MLP(input_size=5, output_size=1)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.BCELoss()  # 이진 분류이므로 Binary Cross Entropy 사용

#4. 모델 학습
def train_model(model, X_train, y_train, epochs=10):
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}, Loss: {loss.item()}")

train_model(model, X_train, y_train, epochs=5)

#5. 모델 예측
with torch.no_grad():
    test_predictions = model(X_test)
    print("Test Predictions:", test_predictions.squeeze().numpy())

