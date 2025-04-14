from flask import Flask, request, jsonify
import tenseal as ts
import base64

app = Flask(__name__)

# 1. 암호화 context 설정
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.global_scale = 2**40
context.generate_galois_keys()

# 2. 선형 모델 파라미터 정의 (Wx + b)
weights = [0.2, 0.4, 0.1]  # w1, w2, w3
bias = 0.5                 # b

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # 암호화된 입력 받기
        enc_b64 = request.get_json()["enc_input"]
        enc_bytes = base64.b64decode(enc_b64)
        enc_vec = ts.ckks_vector_from(context, enc_bytes)

        # 요소별 곱: Enc(x) * w
        weighted = enc_vec * weights

        print("가중치 곱 결과:", weighted.decrypt())

        # 합계 + bias: w1*x1 + w2*x2 + w3*x3 + b
        enc_result = weighted.sum() + bias

        print("합계 + bias 결과:", enc_result.decrypt())

        # 결과 직렬화 후 base64 인코딩
        result_bytes = enc_result.serialize()
        result_b64 = base64.b64encode(result_bytes).decode("utf-8")

        return jsonify({"enc_result": result_b64})

    except Exception as e:
        print("서버 오류:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
