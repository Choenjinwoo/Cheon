# crypto_test.py
import tenseal as ts

# 1. 암호화 context 설정
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.global_scale = 2**40
context.generate_galois_keys()

# 2. 암호화할 벡터 데이터
plain_vec = [1.0, 2.0, 3.0]

# 3. CKKS 벡터 암호화
enc_vec = ts.ckks_vector(context, plain_vec)

# 4. 암호화된 벡터에 연산 수행
enc_result = enc_vec * 5 + 1  # (각 원소에 *5 + 1)

# 5. 복호화
decrypted = enc_result.decrypt()

print("복호화된 결과:", decrypted)
