# crypto_test.py
import tenseal as ts

# 1. 암호화 context 생성
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.global_scale = 2**40
context.generate_galois_keys()

# 2. 평문 입력 벡터
plain_vec = [1.0, 2.0, 3.0, 4.0]

# 3. 암호화
enc_vec = ts.ckks_vector(context, plain_vec)

# 4. 암호화된 상태에서 연산
enc_result = (enc_vec + 1) * 2

# 5. 복호화
decrypted_result = enc_result.decrypt()

print("복호화된 결과:", decrypted_result)
