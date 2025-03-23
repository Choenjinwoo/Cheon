import requests
import json

# ✅ Flask 서버 주소 설정
server_url = "http://127.0.0.1:5001/predict"  # 서버가 실행 중인 주소 확인

# ✅ 테스트용 암호화된 데이터 (나중에 실제 동형 암호 데이터로 변경 예정)
data = {
    "encrypted_data": [3.5, 2.1, -1.2, 0.7, 4.0]
}

try:
    print("서버에 요청 보내는 중...")

    # ✅ 서버에 POST 요청 보내기 (timeout 추가)
    response = requests.post(server_url, json=data, timeout=5)

    # ✅ HTTP 응답 상태 코드 확인
    response.raise_for_status()  # 오류 발생 시 예외 처리

    # ✅ 서버 응답 출력
    print("서버 응답:", response.json())

except requests.exceptions.Timeout:
    print("서버 응답 시간 초과! Flask 서버가 실행 중인지 확인하세요.")

except requests.exceptions.ConnectionError:
    print("서버에 연결할 수 없습니다! Flask 서버가 실행되고 있는지 확인하세요.")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP 오류 발생: {http_err}")

except requests.exceptions.RequestException as e:
    print(f"요청 중 오류 발생: {e}")
