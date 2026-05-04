import random
from operations_maths import expo_modulaire, inverse_modulo


def coder_bloc(m, public_key):
    p, g, y = public_key

    k = random.randint(2, p - 2)

    c1 = expo_modulaire(g, k, p)
    c2 = (m * expo_modulaire(y, k, p)) % p

    return (c1, c2)


def decoder_bloc(cipher, private_key, public_key):
    c1, c2 = cipher
    p, _, _ = public_key

    s = expo_modulaire(c1, private_key, p)
    s_inv = inverse_modulo(s, p)

    return (c2 * s_inv) % p