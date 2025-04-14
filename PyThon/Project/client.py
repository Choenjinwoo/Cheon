import tenseal as ts
import base64
import requests

# 암호화 context 생성
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.global_scale = 2**40
context.generate_galois_keys()

# 입력 벡터 (예: 나이, 체온, 혈압)
plain_vec = [2, 2, 3]
enc_vec = ts.ckks_vector(context, plain_vec)

# 직렬화 후 base64 인코딩
enc_bytes = enc_vec.serialize()
enc_b64 = base64.b64encode(enc_bytes).decode("utf-8")

# 서버로 POST 요청 보내기
response = requests.post("http://127.0.0.1:5000/predict", json={"enc_input": enc_b64})

try:
    response_json = response.json()
    if "enc_result" in response_json:
        result_b64 = response_json["enc_result"]
        result_bytes = base64.b64decode(result_b64)
        enc_result = ts.ckks_vector_from(context, result_bytes)
        print("복호화된 결과:", enc_result.decrypt())
    else:
        print("서버 응답 오류:", response_json.get("error", "알 수 없는 오류"))
except Exception as e:
    print("❗ 예외 발생:", e)
    print("서버 응답:", response.text)
