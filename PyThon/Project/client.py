import base64
import requests
from crypto_utils import load_context, encrypt_vector, decrypt_vector

context = load_context()
print("context scale:", context.global_scale)

plain_vec = [2.0, 4.0, 8.0]
print("보낸 입력값:", plain_vec)

enc_vec = encrypt_vector(context, plain_vec)
enc_bytes = enc_vec.serialize()
enc_b64 = base64.b64encode(enc_bytes).decode("utf-8")

response = requests.post("http://127.0.0.1:5000/predict", json={"enc_input": enc_b64})

try:
    response_json = response.json()
    if "enc_result" in response_json:
        result_b64 = response_json["enc_result"]
        result_bytes = base64.b64decode(result_b64)
        enc_result = decrypt_vector(context, result_bytes)
        print("복호화된 결과:", enc_result.decrypt())
    else:
        print("서버 응답 오류:", response_json.get("error", "알 수 없는 오류"))
except Exception as e:
    print("❗ 예외 발생:", e)
    print("📨 서버 응답 원본:", response.text)
