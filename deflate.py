class HuffmanNode:
    def __init__(self, freq, data, left=None, right=None):
        self.freq = freq
        self.data = data
        self.left = left
        self.right = right

def freq_map(message):    
    dico = {}
    for c in message:
        if c in dico:
            dico[c] += 1
        else:
            dico[c] = 1
    return dico


def generate_tree(freq_map):

    list_nodes = {}
    for c in freq_map:
        list_nodes[HuffmanNode(freq_map[c],c)] = freq_map[c]
    

    def pop_min():
        mini = min(list_nodes.values())
        min_node = None
        for node in list_nodes:
            if node.freq == mini:
                min_node = node 
        list_nodes.pop(min_node)
        return min_node

    while (len(list_nodes)>1):
        min_node = pop_min()
        min2_node = pop_min()
        node = HuffmanNode(min_node.freq+min2_node.freq, '' , left=min_node, right=min2_node)
        list_nodes[node] = min_node.freq+min2_node.freq
       
    
    return list(list_nodes.keys())[0]



def set_binary_code(node, prefix, mapping):
    if node.left ==None and node.right ==None: 
        mapping[node.data] = prefix    
    else:             
        set_binary_code(node.left, prefix+'0', mapping)
        set_binary_code(node.right, prefix+'1',mapping)




def lempelziv(uncompressed):

    dict_size = 256
    dico = dict((chr(i), i) for i in range(dict_size))
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dico:
            w = wc
        else:
            result.append(dico[w])
            dico[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        result.append(dico[w])
    return result, dico

s = "fheizmezajmezajimzeajimomoimimim"


def deflate(message: str) -> tuple[str, dict, HuffmanNode]:

    codeLZ, dicoLZ = lempelziv(message)
    print("Code par Lempel-Ziv",codeLZ)

    dico = {}
    frequences = freq_map(codeLZ)
    print("Dico de fréquences ",frequences)
    arbre = generate_tree(frequences)
    set_binary_code(arbre,'', dico)
    print("Dictionnaire de l'arbre d'Huffman ",dico)

    result = ''
    for c in codeLZ:
        result += dico[c]
    return result, dico, arbre

r,_,_ = deflate(s)
print(r)


