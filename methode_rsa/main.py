import sys
import os

# Ajoute le dossier courant au path pour éviter le conflit
# avec le package Python standard "methode_rsa"
sys.path.insert(0, os.path.dirname(__file__))

from rsa import coder_bloc, decoder_bloc  # noqa: E402 (import local)
from generation_cles import produire_cles
from utils import conversion_texte_blocs, conversion_blocs_texte


def main():
    print("=== RSA ===")

    try:
        public_key, private_key = produire_cles()

        print("\nClé publique (e, n) :", public_key)
        print("Clé privée  (d, n) :", private_key)

        text = input("\nEntrer le message : ")

        e, n = public_key

        # block_size=1 : chaque bloc = ord(c) ≤ 255, toujours < n (min ~65000)
        block_size = 1
        blocks = conversion_texte_blocs(text, block_size)

        # Vérification défensive
        problematic = [chr(b) for b in blocks if b >= n]
        if problematic:
            print(f"Erreur : les caractères {problematic} ont une valeur >= n={n}.")
            return

        cipher = [coder_bloc(b, public_key) for b in blocks]
        print("\nChiffré :", cipher)

        decrypted_blocks = [decoder_bloc(c, private_key) for c in cipher]
        result = conversion_blocs_texte(decrypted_blocks)

        print("\nDéchiffré :", result)
        print("Vérification :", "✓ OK" if result == text else "✗ ÉCHEC")

    except Exception as e:
        print("Erreur inattendue :", e)


if __name__ == "__main__":
    main()