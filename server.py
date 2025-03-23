import signal
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS 허용 (브라우저에서도 요청 가능)

# ✅ 기본 페이지 추가 (루트 엔드포인트 처리)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask 서버가 정상적으로 실행 중입니다!"})

# ✅ 서버 정상 작동 확인용 엔드포인트 (GET 요청)
@app.route('/test', methods=['GET'])
def test_api():
    return jsonify({"message": "서버 연결 성공!"})

# ✅ 클라이언트에서 데이터 전송을 테스트하는 엔드포인트 (POST 요청)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 🔹 클라이언트에서 보낸 JSON 데이터 받기
        data = request.get_json()  # request.json과 동일
        if not data:  # 데이터가 없는 경우 오류 처리
            print("🚨 오류: 요청 본문이 비어 있음")
            return jsonify({"error": "요청 데이터가 없습니다."}), 400

        encrypted_data = data.get("encrypted_data", [])  # "encrypted_data" 키가 없을 경우 빈 리스트 반환
        print("🔒 받은 데이터:", encrypted_data)  # 터미널에 로그 출력 (디버깅 용도)

        # 🔹 서버가 받은 데이터에 대한 응답 생성
        response = {
            "message": "데이터 수신 성공",
            "received_data": encrypted_data
        }

        return jsonify(response), 200  # 정상 응답 반환

    except Exception as e:
        print("🚨 서버 오류 발생:", str(e))  # 서버에서 오류 발생 시 출력
        return jsonify({"error": "서버 내부 오류 발생"}), 500
    
def signal_handler(sig, frame):
    print("🚨 강제 종료 감지됨! 서버를 안전하게 종료합니다.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ✅ 서버 실행 (포트 5000, 디버그 모드 활성화)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001, debug=True)

