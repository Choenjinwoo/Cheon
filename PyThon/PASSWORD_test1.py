import tenseal as ts

#동형 암호화 컨텍스트 생성
context = ts.context(
    scheme=ts.SCHEME_TYPE.CKKS,  # 실수 연산을 지원하는 CKKS 방식 사용
    poly_modulus_degree=8192,  # 암호화 강도 조절 (4096, 8192, 16384 가능)
    coeff_mod_bit_sizes=[60, 40, 40, 60]  # 암호화 강도 설정
)
context.global_scale = 2**40  # 암호화된 데이터의 연산 정밀도
context.generate_galois_keys()  # 행렬 연산 지원

print("동형 암호화 컨텍스트 생성 완료")

# ✅ 암호화할 데이터
vector = [3.5, 2.1, -1.2, 0.7, 4.0]

# ✅ 벡터 암호화
encrypted_vector = ts.ckks_vector(context, vector)
print("암호화된 데이터:", encrypted_vector.serialize())

# ✅ 복호화 테스트
decrypted_vector = encrypted_vector.decrypt()
print("복호화된 데이터:", decrypted_vector)

# ✅ 암호화된 데이터 연산 테스트
encrypted_vector_2 = ts.ckks_vector(context, [1.0, 1.0, 1.0, 1.0, 1.0])

# ✅ 벡터 덧셈 연산 (암호화된 상태에서 수행)
encrypted_sum = encrypted_vector + encrypted_vector_2
print("암호화된 덧셈 결과:", encrypted_sum.decrypt())

# ✅ 벡터 곱셈 연산 (암호화된 상태에서 수행)
encrypted_mul = encrypted_vector * 2
print("암호화된 곱셈 결과:", encrypted_mul.decrypt())