def expo_modulaire(base, exp, mod):
    result = 1
    base %= mod

    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1

    return result


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def inverse_modulo(a, mod):
    g, x, _ = extended_gcd(a, mod)
    if g != 1:
        return None
    return x % mod