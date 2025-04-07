# server.py
from flask import Flask, request, jsonify
import tenseal as ts
import base64

app = Flask(__name__)

# 서버 context 설정 (클라이언트와 동일하게)
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.global_scale = 2**40
context.generate_galois_keys()

@app.route("/predict", methods=["POST"])
def predict():
    # 1. 클라이언트로부터 암호화된 입력 받기
    enc_b64 = request.get_json()["enc_input"]

    # 2. base64 디코딩 → 역직렬화
    enc_bytes = base64.b64decode(enc_b64)
    enc_vec = ts.ckks_vector_from(context, enc_bytes)

    # 3. 암호화된 상태에서 연산 수행 (예: (x + 1) * 2)
    enc_result = (enc_vec + 1) * 2

    # 4. 결과 직렬화 및 base64 인코딩
    result_bytes = enc_result.serialize()
    result_b64 = base64.b64encode(result_bytes).decode("utf-8")

    # 5. 응답 반환
    return jsonify({"enc_result": result_b64})

if __name__ == '__main__':
    app.run(port=5000)
