from operations_maths import expo_modulaire


def coder_bloc(m, public_key):
    e, n = public_key
    return expo_modulaire(m, e, n)


def decoder_bloc(c, private_key):
    d, n = private_key
    return expo_modulaire(c, d, n)