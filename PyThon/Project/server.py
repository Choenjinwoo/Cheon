from flask import Flask, request, jsonify
from crypto_utils import create_context
from handler import process_encrypted_request

app = Flask(__name__)

context = create_context()
print("context scale:", context.global_scale)
weights = [0.2, 0.1, 0.1]
bias = 0.1

@app.route("/predict", methods=["POST"])
def predict():
    try:
        enc_b64 = request.get_json()["enc_input"]
        result_b64 = process_encrypted_request(context, enc_b64, weights, bias)
        return jsonify({"enc_result": result_b64})
    except Exception as e:
        import traceback
        print("❗ 서버 오류 발생:")
        traceback.print_exc()  # ← 에러 전체 출력!
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)