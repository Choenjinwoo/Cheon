def linear_predict(enc_vec, weights, bias):
    weighted = enc_vec * weights
    return weighted.sum() + bias