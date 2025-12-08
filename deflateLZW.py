
def lempelziv(uncompressed):
    """Compresse le message uncompressed avec l'algorithme LZW
        Renvoie le code et le dictionnaire 
    """

    dict_size = 256
    dico = dict((chr(i), i) for i in range(dict_size))
    suite_cara = ""
    result = []
    for cara in uncompressed:
        suite = suite_cara + cara
        if suite in dico:
            suite_cara = suite
        else:
            result.append(dico[suite_cara])
            dico[suite] = dict_size
            dict_size += 1
            suite_cara = cara
    if suite_cara:
        result.append(dico[suite_cara])
    return result

def deflateLZW(message: str) -> tuple[str, dict, huff]:
    """Deflate algorithme utilisant compression LZW + Huffman
    """

    codeLZ = lempelziv(message)

    dico = {}
    frequences = huff.freq_map(codeLZ)
    arbre = huff.generate_tree(frequences)
    huff.set_binary_code(arbre,'', dico)

    result = ''
    for c in codeLZ:
        result += dico[c]
    return result, dico, arbre

def inflateLZW(code, root):
    """Inverse de deflateLZW 
    """

    dict_size = 256
    dico = dict((i,chr(i)) for i in range(dict_size))

    message = ''
    w = ""
    node = root
    for bit in code:
        node = node.left if bit == '0' else node.right
        if node.left is None and node.right is None:
            message += dico[node.data]
            c = dico[node.data]
            node = root
            wc = w + c
            if wc in dico.values():
                w = wc
            else:
                dico[dict_size] = wc
                dict_size += 1
                w = c
    return message





