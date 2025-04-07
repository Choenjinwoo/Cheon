# client.py
import tenseal as ts
import base64
import requests

# 1. 암호화 context 생성
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.global_scale = 2**40
context.generate_galois_keys()

# 2. 벡터 암호화
plain_vec = [1.0, 2.0, 3.0]
enc_vec = ts.ckks_vector(context, plain_vec)

# 3. 직렬화 후 base64 인코딩 (문자열화)
enc_bytes = enc_vec.serialize()
enc_b64 = base64.b64encode(enc_bytes).decode("utf-8")

# 4. JSON 데이터 전송
payload = {"enc_input": enc_b64}
response = requests.post("http://127.0.0.1:5000/predict", json=payload)

# 5. 응답 받은 암호화된 결과 복호화
result_b64 = response.json()["enc_result"]
result_bytes = base64.b64decode(result_b64)
enc_result = ts.ckks_vector_from(context, result_bytes)

print("복호화된 결과:", enc_result.decrypt())
