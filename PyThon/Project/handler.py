from crypto_utils import decrypt_vector, serialize_vector
from linear_model import linear_predict
import base64

def process_encrypted_request(context, enc_b64, weights, bias):
    enc_bytes = base64.b64decode(enc_b64)
    enc_vec = decrypt_vector(context, enc_bytes)
    enc_result = linear_predict(enc_vec, weights, bias)
    return serialize_vector(enc_result)