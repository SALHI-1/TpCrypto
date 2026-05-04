from elgamal import coder_bloc, decoder_bloc
from generation_cles import produire_cles
from utils import conversion_texte_blocs, conversion_blocs_texte


def main():
    print("=== ELGAMAL ===")

    try:
        public_key, private_key = produire_cles()

        print("\nClé publique (p, g, y) :", public_key)
        print("Clé privée   (x)       :", private_key)

        text = input("\nEntrer le message : ")

        blocks = conversion_texte_blocs(text)

        p = public_key[0]

        # Vérification : chaque valeur de caractère doit être < p
        problematic = [(chr(b), b) for b in blocks if b >= p]
        if problematic:
            chars_str = ", ".join(f"'{c}' (={v})" for c, v in problematic)
            print(f"Erreur : les caractères {chars_str} ont une valeur >= p={p}.")
            print("Conseil : utiliser uniquement des caractères de valeur < p.")
            return

        cipher = [coder_bloc(b, public_key) for b in blocks]

        print("\nChiffré :", cipher)

        decrypted_blocks = [
            decoder_bloc(c, private_key, public_key)
            for c in cipher
        ]

        result = conversion_blocs_texte(decrypted_blocks)

        print("\nDéchiffré :", result)
        print("Vérification :", "✓ OK" if result == text else "✗ ÉCHEC")

    except Exception as e:
        print("Erreur inattendue :", e)


if __name__ == "__main__":
    main()