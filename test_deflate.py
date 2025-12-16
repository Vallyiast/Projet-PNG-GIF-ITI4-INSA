import deflate
from huffman_node import HuffmanNode as huff
import pytest

s = "code code code code"
t = "lorem ipsum versi color colem ispum veri color"
lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit."

#Liste (correctes) provenant d'arbres
list_len = [0, 5, 4, 1, 0, 4, 0, 0, 0, 3, 0, 3, 0, 4, 0, 0, 0, 5, 0]
list_len2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 4, 0, 0, 5, 4, 0, 4, 4, 0, 4, 3, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 4, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
dict_len = {0: '0', 1: '11110', 3: '1100', 4: '100', 5: '101', 7: '1101', 17: '11111', 18: '1110'}
dict_len2 = {32: '000', 99: '11000', 101: '001', 105: '0110', 108: '11001', 109: '0111', 111: '1000', 112: '1001', 114: '1010', 115: '010', 117: '11010', 118: '11011', 256: '11100', 257: '11101', 258: '1011', 260: '11110', 261: '11111'}

# -------------------- HuffmanNode------------

@pytest.mark.parametrize("dict_arbre", [dict_len,dict_len2])
def test_dict_arbres(dict_arbre):
    arbre = huff.recreate_tree_from_dict(dict_arbre)
    dict_result = dict()
    huff.set_binary_code(arbre, '', dict_result)
    assert dict_arbre == dict_result

@pytest.mark.parametrize("list_longueur", [list_len,list_len2])
def test_huffman_canonique(list_longueur):
    print(list_longueur)
    result_dict = huff.huffman_canonique(list_longueur)
    print([len(result_dict[i]) if i in result_dict else 0 for i in range(len(list_longueur))])
    assert list_longueur == [len(result_dict[i]) if i in result_dict else 0 for i in range(len(list_longueur))]

#-------------Deflate--------------------------

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
def test_decompressionLZ77(message):
    msg = [ord(c) for c in message]
    compr,_, _ = deflate.compressionLZ77(msg)

    decode = deflate.decompressionLZ77([(deflate.conversion_classes_decompression(elt[0][0],deflate.LENGTH_TABLE)[0]+elt[0][1],deflate.conversion_classes_decompression(elt[1][0],deflate.DISTANCE_TABLE)[0]+elt[1][1]) if isinstance(elt, tuple) else elt for elt in compr])

    print("resultat décodage:", decode)
    assert msg == decode

@pytest.mark.parametrize("list_longueur", [list_len, list_len2])
def test_conversion_longueurs_codes(list_longueur):
    result, extra = deflate.conversion_longueurs_symboles(list_longueur)
    final = deflate.inversion_conversion_symbole_longueurs(result,extra)
    assert list_longueur == final

@pytest.mark.parametrize("message", [s,t, lorem])
def test_deflate_data(message):
    """Test la transformation du code de compressionLZ77 par Huffman 
    """
    msg = [ord(c) for c in message]
    compr,list_litt, list_distances = deflate.compressionLZ77(msg)

    arbre_litt = huff.generate_tree_list(list_litt)  #Liste [0-285] des littéraux et des décalages
    dico_litt_temp = {}
    huff.set_binary_code(arbre_litt,'', dico_litt_temp)
    dico_litt = huff.huffman_canonique([len(dico_litt_temp[index]) if index in dico_litt_temp else 0 for index in range(285)])
 
    arbre_distance = huff.generate_tree_list(list_distances) #Liste des longueurs
    dico_distance_temp = {}
    huff.set_binary_code(arbre_distance,'', dico_distance_temp)
    dico_distance = huff.huffman_canonique([len(dico_distance_temp[index]) if index in dico_distance_temp else 0 for index in range(30)])
 
    litlen_tree = huff.recreate_tree_from_dict(dico_litt)
    dist_tree = huff.recreate_tree_from_dict(dico_distance)
    temp_max_lit = max([len(dico_litt_temp[index]) if index in dico_litt_temp else 0 for index in range(285)])
    temp_max_dist = max([len(dico_distance_temp[index]) if index in dico_distance_temp else 0 for index in range(30)])

    print("dictionnaires",dico_litt, dico_distance)

    print("données compressées par LZ:", compr)
    resultat = deflate.deflate_data(compr, dico_litt, dico_distance)
    print("resultat compression", resultat)
    resultatdecompression = deflate.inflate_data(resultat, litlen_tree, dist_tree, temp_max_lit, temp_max_dist)
    print("resultat décompression", resultatdecompression)

    assert [(deflate.conversion_classes_decompression(elt[0][0],deflate.LENGTH_TABLE)[0]+elt[0][1],deflate.conversion_classes_decompression(elt[1][0],deflate.DISTANCE_TABLE)[0]+elt[1][1]) if isinstance(elt, tuple) else elt for elt in compr] == resultatdecompression

    
#--------- TEST FONCTIONNEL -----------
@pytest.mark.parametrize("message", [s,t, lorem])
def test_deflate(message):
    code = deflate.deflate([ord(c) for c in message])
    result = deflate.inflate(code)
    assert "".join([chr(i) for i in result]) == message


