def conversion_texte_blocs(text):
    blocks = []
    for c in text:
        blocks.append(ord(c))
    return blocks


def conversion_blocs_texte(blocks):
    return ''.join(chr(b) for b in blocks)