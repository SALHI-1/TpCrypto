"""
Point d'entrée  — Projet de Cryptographie
=========================================
Lance l'application, puis l'utilisateur choisit :
  1. RSA
  2. ElGamal
  3. Les deux (comparaison : temps d'exécution, taille du chiffré, etc.)
"""

import importlib.util
import sys
import time
from pathlib import Path

# ─── Chargement dynamique des modules (évite le conflit avec le package
#     Python standard "methode_rsa" qui est installé sur ce système) ─────────────────

BASE = Path(__file__).parent


def _load(module_name: str, file_path: Path):
    """Charge un module Python depuis son chemin absolu."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod  = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


# ─── RSA ────────────────────────────────────────────────────────────────────
rsa_math   = _load("rsa_operations_maths", BASE / "methode_rsa" / "operations_maths.py")
# Alias pour que "from operations_maths import ..." dans generation_cles.py / rsa.py fonctionne
sys.modules["operations_maths"] = rsa_math
rsa_generation_cles = _load("rsa_generation_cles",     BASE / "methode_rsa" / "generation_cles.py")
rsa_noyau   = _load("rsa_noyau",       BASE / "methode_rsa" / "crypto_rsa.py")
rsa_fonctions  = _load("rsa_fonctions",      BASE / "methode_rsa" / "fonctions_utiles.py")

# ─── ElGamal ────────────────────────────────────────────────────────────────
eg_math   = _load("eg_operations_maths", BASE / "methode_elgamal" / "operations_maths.py")
eg_generation_cles = _load("eg_generation_cles",     BASE / "methode_elgamal" / "generation_cles.py")
eg_noyau   = _load("eg_noyau",       BASE / "methode_elgamal" / "crypto_elgamal.py")
eg_fonctions  = _load("eg_fonctions",      BASE / "methode_elgamal" / "fonctions_utiles.py")



# ════════════════════════════════════════════════════════════════════════════
#  SÉPARATEUR VISUEL
# ════════════════════════════════════════════════════════════════════════════

def separator(title: str = "") -> None:
    width = 60
    if title:
        side = (width - len(title) - 2) // 2
        print("\n" + "═" * side + f" {title} " + "═" * side)
    else:
        print("─" * width)


# ════════════════════════════════════════════════════════════════════════════
#  RSA
# ════════════════════════════════════════════════════════════════════════════

def executer_rsa(text: str, verbose: bool = True) -> dict:
    """
    Chiffre et déchiffre `text` avec RSA.

    Retourne un dictionnaire de métriques :
      - generation_cles_time   (float) : temps de génération des clés en ms
      - encrypt_time  (float) : temps de chiffrement en ms
      - decrypt_time  (float) : temps de déchiffrement en ms
      - total_time    (float) : temps total en ms
      - cipher_size   (int)   : nombre d'entiers dans le chiffré
      - success       (bool)  : correspondance texte original / décrypté
    """
    # ── Génération des clés ──────────────────────────────────────────────
    t0 = time.perf_counter()
    public_key, private_key = rsa_generation_cles.produire_cles()
    generation_cles_time = (time.perf_counter() - t0) * 1000

    e, n = public_key
    d, _ = private_key

    if verbose:
        separator("RSA — Clés")
        print(f"  Clé publique  (e, n) : ({e}, {n})")
        print(f"  Clé privée   (d, n) : ({d}, {n})")

    # ── Encodage en blocs ────────────────────────────────────────────────
    # block_size=1 → chaque bloc = ord(c) ≤ 127, toujours < n_min (~10100)
    BLOCK_SIZE = 1
    blocks = rsa_fonctions.conversion_texte_blocs(text, BLOCK_SIZE)

    # Vérification défensive (ne devrait pas arriver avec ASCII et block_size=1)
    if any(b >= n for b in blocks):
        raise ValueError(
            f"RSA : un bloc ({max(blocks)}) dépasse n={n}. "
            "Le message contient peut-être des caractères non-ASCII."
        )

    # ── Chiffrement ──────────────────────────────────────────────────────
    t1 = time.perf_counter()
    cipher = [rsa_noyau.coder_bloc(b, public_key) for b in blocks]
    encrypt_time = (time.perf_counter() - t1) * 1000

    if verbose:
        separator("RSA — Chiffrement")
        print(f"  Chiffré (blocs) : {cipher}")

    # ── Déchiffrement ────────────────────────────────────────────────────
    t2 = time.perf_counter()
    decrypted_blocks = [rsa_noyau.decoder_bloc(c, private_key) for c in cipher]
    decrypt_time = (time.perf_counter() - t2) * 1000

    result = rsa_fonctions.conversion_blocs_texte(decrypted_blocks)

    if verbose:
        separator("RSA — Résultat")
        print(f"  Message original : {text!r}")
        print(f"  Message décrypté : {result!r}")
        ok = "✓ SUCCÈS" if result == text else "✗ ÉCHEC"
        print(f"  Vérification     : {ok}")

    total_time = generation_cles_time + encrypt_time + decrypt_time

    return {
        "generation_cles_time":  generation_cles_time,
        "encrypt_time": encrypt_time,
        "decrypt_time": decrypt_time,
        "total_time":   total_time,
        "cipher_size":  len(cipher),
        "success":      result == text,
    }


# ════════════════════════════════════════════════════════════════════════════
#  ELGAMAL
# ════════════════════════════════════════════════════════════════════════════

def executer_elgamal(text: str, verbose: bool = True) -> dict:
    """
    Chiffre et déchiffre `text` avec ElGamal.

    Retourne les mêmes métriques que executer_rsa().
    """
    # ── Génération des clés ──────────────────────────────────────────────
    t0 = time.perf_counter()
    public_key, private_key = eg_generation_cles.produire_cles()
    generation_cles_time = (time.perf_counter() - t0) * 1000

    p, g, y = public_key

    if verbose:
        separator("ElGamal — Clés")
        print(f"  Clé publique (p, g, y) : ({p}, {g}, {y})")
        print(f"  Clé privée   (x)       : {private_key}")

    # ── Encodage en blocs (1 bloc = 1 caractère) ─────────────────────────
    blocks = eg_fonctions.conversion_texte_blocs(text)

    if any(b >= p for b in blocks):
        problematic = [(chr(b), b) for b in blocks if b >= p]
        chars_str = ", ".join(f"'{c}' (valeur={v})" for c, v in problematic)
        raise ValueError(
            f"ElGamal : les caractères {chars_str} ont une valeur >= p={p}. "
            "Utiliser uniquement des caractères dont la valeur < p."
        )

    # ── Chiffrement ──────────────────────────────────────────────────────
    t1 = time.perf_counter()
    cipher = [eg_noyau.coder_bloc(b, public_key) for b in blocks]
    encrypt_time = (time.perf_counter() - t1) * 1000

    if verbose:
        separator("ElGamal — Chiffrement")
        print(f"  Chiffré (paires c1, c2) : {cipher}")

    # ── Déchiffrement ────────────────────────────────────────────────────
    t2 = time.perf_counter()
    decrypted_blocks = [
        eg_noyau.decoder_bloc(c, private_key, public_key) for c in cipher
    ]
    decrypt_time = (time.perf_counter() - t2) * 1000

    result = eg_fonctions.conversion_blocs_texte(decrypted_blocks)

    if verbose:
        separator("ElGamal — Résultat")
        print(f"  Message original : {text!r}")
        print(f"  Message décrypté : {result!r}")
        ok = "✓ SUCCÈS" if result == text else "✗ ÉCHEC"
        print(f"  Vérification     : {ok}")

    total_time = generation_cles_time + encrypt_time + decrypt_time

    return {
        "generation_cles_time":  generation_cles_time,
        "encrypt_time": encrypt_time,
        "decrypt_time": decrypt_time,
        "total_time":   total_time,
        # ElGamal double la taille : chaque bloc → (c1, c2)
        "cipher_size":  len(cipher) * 2,
        "success":      result == text,
    }


# ════════════════════════════════════════════════════════════════════════════
#  COMPARAISON
# ════════════════════════════════════════════════════════════════════════════

def lancer_comparaison(text: str) -> None:
    """Lance RSA et ElGamal sur le même texte et affiche un tableau comparatif."""
    separator("COMPARAISON RSA vs ElGamal")
    print(f"  Message testé : {text!r}  ({len(text)} caractères)\n")

    print("  ⏳ Exécution de RSA ...")
    try:
        rsa_metrics = executer_rsa(text, verbose=False)
        rsa_ok = rsa_metrics["success"]
    except ValueError as err:
        print(f"  ✗ RSA a échoué : {err}")
        rsa_metrics = None
        rsa_ok = False

    print("  ⏳ Exécution de ElGamal ...")
    try:
        eg_metrics = executer_elgamal(text, verbose=False)
        eg_ok = eg_metrics["success"]
    except ValueError as err:
        print(f"  ✗ ElGamal a échoué : {err}")
        eg_metrics = None
        eg_ok = False

    # ── Tableau récapitulatif ────────────────────────────────────────────
    separator("Résultats")

    col_w = 22
    header = (
        f"  {'Métrique':<{col_w}} {'RSA':>12} {'ElGamal':>12}"
    )
    print(header)
    print("  " + "─" * (col_w + 26))

    def row(label: str, rsa_val, eg_val, unit: str = "") -> None:
        rv = f"{rsa_val:.3f}{unit}" if rsa_metrics and rsa_val is not None else "N/A"
        ev = f"{eg_val:.3f}{unit}"  if eg_metrics  and eg_val  is not None else "N/A"
        print(f"  {label:<{col_w}} {rv:>12} {ev:>12}")

    def row_int(label: str, rsa_val, eg_val, unit: str = "") -> None:
        rv = f"{rsa_val}{unit}" if rsa_metrics and rsa_val is not None else "N/A"
        ev = f"{eg_val}{unit}"  if eg_metrics  and eg_val  is not None else "N/A"
        print(f"  {label:<{col_w}} {rv:>12} {ev:>12}")

    if rsa_metrics and eg_metrics:
        row("Génération clés (ms)",  rsa_metrics["generation_cles_time"],  eg_metrics["generation_cles_time"])
        row("Chiffrement (ms)",      rsa_metrics["encrypt_time"], eg_metrics["encrypt_time"])
        row("Déchiffrement (ms)",    rsa_metrics["decrypt_time"], eg_metrics["decrypt_time"])
        row("Temps total (ms)",      rsa_metrics["total_time"],   eg_metrics["total_time"])
        row_int("Taille chiffré (entiers)", rsa_metrics["cipher_size"], eg_metrics["cipher_size"])
        row_int("Succès déchiffrement",
                "✓ OUI" if rsa_ok else "✗ NON",
                "✓ OUI" if eg_ok else "✗ NON")


# ════════════════════════════════════════════════════════════════════════════
#  MENU PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

MENU = """
╔══════════════════════════════════════════╗
║      TP CRYPTOGRAPHIE — RSA & ElGamal   ║
╠══════════════════════════════════════════╣
║  1. RSA                                 ║
║  2. ElGamal                             ║
║  3. Comparaison RSA vs ElGamal          ║
║  0. Quitter                             ║
╚══════════════════════════════════════════╝
"""


def get_choice(prompt: str, valid: set) -> str:
    while True:
        val = input(prompt).strip()
        if val in valid:
            return val
        print(f"  ✗ Choix invalide. Options : {sorted(valid)}")


def main() -> None:
    print(MENU)

    while True:
        choice = get_choice("Votre choix : ", {"0", "1", "2", "3"})

        if choice == "0":
            print("\n  À bientôt !\n")
            break

        text = input("\nEntrer le message à chiffrer : ").strip()
        if not text:
            print("  ✗ Le message ne peut pas être vide.")
            continue

        print()
        try:
            if choice == "1":
                executer_rsa(text)
            elif choice == "2":
                executer_elgamal(text)
            elif choice == "3":
                lancer_comparaison(text)
        except ValueError as err:
            print(f"\n  ✗ Erreur : {err}")
        except Exception as err:
            print(f"\n  ✗ Erreur inattendue : {err}")

        print()
        again = get_choice("\nRecommencer ? (o/n) : ", {"o", "n"})
        if again == "n":
            print("\n  À bientôt !\n")
            break
        print(MENU)


if __name__ == "__main__":
    main()
