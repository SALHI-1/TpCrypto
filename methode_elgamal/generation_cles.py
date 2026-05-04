import random
from operations_maths import expo_modulaire


def test_primalite(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def creer_premier():
    while True:
        n = random.randint(256, 500)
        if test_primalite(n):
            return n


def _prime_factors(n: int) -> list:
    """Retourne les facteurs premiers distincts de n."""
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def find_generator(p: int) -> int:
    """
    Trouve un générateur du groupe cyclique Z_p* en O(p·log p).

    Un entier g est un générateur si et seulement si, pour chaque
    facteur premier q de (p−1), on a g^((p−1)/q) ≢ 1 (mod p).
    """
    order = p - 1
    factors = _prime_factors(order)

    for g in range(2, p):
        if all(expo_modulaire(g, order // q, p) != 1 for q in factors):
            return g

    return 2  # repli de sécurité (ne devrait jamais arriver)


def produire_cles():
    p = creer_premier()
    g = find_generator(p)

    x = random.randint(2, p - 2)
    y = expo_modulaire(g, x, p)

    return (p, g, y), x