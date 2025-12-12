import deflate
from huffman_node import HuffmanNode as huff
import pytest

s = "code code code code"
t = "lorem ipsum versi color colem ispum veri color"
lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit."

list_len = [0, 5, 4, 1, 0, 4, 0, 0, 0, 3, 0, 3, 0, 4, 0, 0, 0, 5, 0]
list_len2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 4, 0, 0, 5, 4, 0, 4, 4, 0, 4, 3, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 4, 0, 5, 5, 0, 0, 0, 0, 1, 0, 0, 0, 1]

dict_len = {0: '0', 1: '11110', 3: '1100', 4: '100', 5: '101', 7: '1101', 17: '11111', 18: '1110'}
dict_len2 = {32: '000', 99: '11000', 101: '001', 105: '0110', 108: '11001', 109: '0111', 111: '1000', 112: '1001', 114: '1010', 115: '010', 117: '11010', 118: '11011', 256: '11100', 257: '11101', 258: '1011', 260: '11110', 261: '11111'}

@pytest.mark.parametrize("message", [s,t,lorem])
def test_coherence_maps_data(message):
    compr,list_litt, list_dist = deflate.compressionLZ77([ord(c) for c in message])

    map_dist = {i:list_dist[i] for i in range(len(list_dist)) if list_dist[i]>0}
    map_litt = {i:list_litt[i] for i in range(len(list_litt)) if list_litt[i]>0}

    map_litt_huff = huff.freq_map([c[0][0] if isinstance(c,tuple) else c for c in compr ])
    map_dist_huff = huff.freq_map([c[1][0] for c in compr  if isinstance(c,tuple)])

    assert map_litt == map_litt_huff
    assert map_dist_huff == map_dist

@pytest.mark.parametrize("message", [s,t,lorem])
def test_coherence_caracteres(message):
    """Vérifie que tous les caractères du message apparaissent bien au moins une fois dans le résultat de compression
    """
    msg = [ord(c) for c in message]
    compr,list_litt, list_dist = deflate.compressionLZ77(msg)
    fl = True
    for c in msg:
        flag = False
        for d in compr:
            if c == d:
                flag = True
                break
        if not flag:
            fl = False
            break
    assert flag

@pytest.mark.parametrize("message", [s,t])
def test_decompression(message):
    msg = [ord(c) for c in message]
    compr,_, _ = deflate.compressionLZ77(msg)
    decode = deflate.decompressionLZ77(compr)

    print("resultat décodage:", decode)
    assert msg == decode

# -------------------- HuffmanNode------------

@pytest.mark.parametrize("dict_arbre", [dict_len,dict_len2])
def test_dict_arbres(dict_arbre):
    arbre = huff.recreate_tree_from_dict(dict_arbre)
    dict_result = dict()
    huff.set_binary_code(arbre, '', dict_result)
    assert dict_arbre == dict_result

@pytest.mark.parametrize("list_longueur", [list_len,list_len2])
def test_huffman_canonique(list_longueur):
    result_dict = huff.huffman_canonique(list_longueur)
    assert list_longueur == [len(result_dict[i]) if i in result_dict else 0 for i in range(len(list_longueur))]

@pytest.mark.parametrize("list_longueur", [[0, 0, 3, 1, 0, 4, 0, 5, 0, 4, 0, 3, 0, 4, 0, 0, 0, 5, 0]])
def test_conversion_longueurs_codes(list_longueur):
    result, extra = deflate.conversion_longueurs_symboles(list_longueur)
    final = deflate.inversion_conversion_symbole_longueurs(result,extra)
    assert list_longueur == final
