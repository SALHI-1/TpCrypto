# TpCrypto

Ce projet est un TP de cryptographie implémentant les méthodes de chiffrement asymétrique **RSA** et **ElGamal**.

## Structure du projet

Le code est divisé en deux modules principaux :

### 1. Méthode RSA (`methode_rsa/`)
- `generation_cles.py` : Génération des clés (publique et privée).
- `crypto_rsa.py` : Logique de chiffrement et de déchiffrement.
- `operations_maths.py` : Opérations mathématiques (pgcd, primalité, exponentiation modulaire, etc.).
- `fonctions_utiles.py` : Outils et fonctions d'aide.
- `main.py` : Script de test ou d'exécution pour la méthode RSA.

### 2. Méthode ElGamal (`methode_elgamal/`)
- `generation_cles.py` : Génération des clés (publique et privée) avec paramètres (p, g).
- `crypto_elgamal.py` : Logique de chiffrement et de déchiffrement.
- `operations_maths.py` : Opérations mathématiques spécifiques.
- `fonctions_utiles.py` : Outils et fonctions d'aide.
- `main.py` : Script de test ou d'exécution pour la méthode ElGamal.

### Point d'entrée global
- `main.py` (à la racine) : Script principal pour lancer et interagir avec les deux implémentations cryptographiques.

## Prérequis

- **Python 3.x** installé sur votre machine.

## Comment l'utiliser

Vous pouvez exécuter indépendamment les algorithmes ou utiliser le script principal :

```bash
# Pour utiliser RSA spécifiquement
python methode_rsa/main.py

# Pour utiliser ElGamal spécifiquement
python methode_elgamal/main.py

# Pour lancer le script global
python main.py
```
