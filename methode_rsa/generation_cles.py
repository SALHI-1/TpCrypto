import random
from operations_maths import inverse_modulo


def test_primalite(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def creer_premier(min_val=256, max_val=500):
    while True:
        n = random.randint(min_val, max_val)
        if test_primalite(n):
            return n


def creer_exposant(phi):
    e = 3
    while e < phi:
        if inverse_modulo(e, phi) is not None:
            return e
        e += 2
    raise Exception("Impossible de générer e")


def produire_cles():
    p = creer_premier()
    q = creer_premier()

    while p == q:
        q = creer_premier()

    n = p * q
    phi = (p - 1) * (q - 1)

    e = creer_exposant(phi)
    d = inverse_modulo(e, phi)

    return (e, n), (d, n)