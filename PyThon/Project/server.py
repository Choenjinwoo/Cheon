# server.py
from flask import Flask, request, jsonify
import tenseal as ts
import base64
import torch
from model import SimpleModel

app = Flask(__name__)

# 암호화 context 설정
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.global_scale = 2**40
context.generate_galois_keys()

# AI 모델 불러오기
model = SimpleModel()
model.load_state_dict(torch.load("model.pt"))
model.eval()

@app.route("/predict", methods=["POST"])
def predict():
    try:
        enc_b64 = request.get_json()["enc_input"]
        enc_bytes = base64.b64decode(enc_b64)
        enc_vec = ts.ckks_vector_from(context, enc_bytes)

        # 암호화 벡터를 리스트로 변환 → 텐서
        input_tensor = torch.tensor(enc_vec.tolist(), dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            output = model(input_tensor)
            result = output.item()

        enc_result = ts.ckks_vector(context, [result])
        result_bytes = enc_result.serialize()
        result_b64 = base64.b64encode(result_bytes).decode("utf-8")

        return jsonify({"enc_result": result_b64})

    except Exception as e:
        print("서버 오류:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
