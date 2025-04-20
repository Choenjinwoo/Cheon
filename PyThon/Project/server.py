from flask import Flask, request, jsonify
from crypto_utils import create_context, save_context
from handler import process_encrypted_request

app = Flask(__name__)

# context 생성 및 저장
context = create_context()
save_context(context)  # 파일로 저장해서 클라이언트가 공유하도록

weights = [0.2, 0.4, 0.1]
bias = 0.5

@app.route("/predict", methods=["POST"])
def predict():
    try:
        enc_b64 = request.get_json()["enc_input"]
        result_b64 = process_encrypted_request(context, enc_b64, weights, bias)
        return jsonify({"enc_result": result_b64})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)