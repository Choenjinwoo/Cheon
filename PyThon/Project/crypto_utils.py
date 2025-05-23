import tenseal as ts
import base64

def create_context():
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.global_scale = 2**40
    context.generate_galois_keys()
    return context

def save_context(context, path="context.tenseal"):
    with open(path, "wb") as f:
        f.write(context.serialize(save_secret_key=True))

def load_context(path="context.tenseal"):
    with open(path, "rb") as f:
        context_bytes = f.read()
    return ts.context_from(context_bytes)

def encrypt_vector(context, plain_vec):
    return ts.ckks_vector(context, plain_vec)

def decrypt_vector(context, enc_bytes):
    return ts.ckks_vector_from(context, enc_bytes)

def serialize_vector(enc_vec):
    return base64.b64encode(enc_vec.serialize()).decode("utf-8")

def deserialize_vector(context, enc_b64):
    enc_bytes = base64.b64decode(enc_b64)
    return ts.ckks_vector_from(context, enc_bytes)