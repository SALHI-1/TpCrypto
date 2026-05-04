def conversion_texte_blocs(text, block_size):
    blocks = []
    for i in range(0, len(text), block_size):
        block = text[i:i+block_size]
        value = 0
        for c in block:
            value = value * 256 + ord(c)
        blocks.append(value)
    return blocks


def conversion_blocs_texte(blocks):
    text = ""

    for block in blocks:
        chars = []
        while block > 0:
            chars.append(chr(block % 256))
            block //= 256
        text += ''.join(reversed(chars))

    return text