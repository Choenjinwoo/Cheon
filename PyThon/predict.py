# predict.py
import torch
from model import SimpleModel  # model.py에서 구조 불러오기

# 모델 불러오기
model = SimpleModel()
model.load_state_dict(torch.load("model.pt"))
model.eval()

# 테스트 입력
test_input = torch.tensor([[32, 37.2, 135]], dtype=torch.float32)

# 예측
prediction = model(test_input)
print("예측 결과:", prediction.item())
