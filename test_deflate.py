import deflate
from huffman_node import HuffmanNode as huff
import pytest

s = "code code code code"
t = "lorem ipsum versi color colem ispum veri color"
lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit."

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


@pytest.mark.parametrize("message", [s,t, lorem])
def test_decompression(message):
    msg = [ord(c) for c in message]
    compr,list_litt, list_dist = deflate.compressionLZ77(msg)
    decode = deflate.decompressionLZ77(compr)
    print(msg)
    print(decode)
    assert msg == decode


@pytest.mark.parametrize("list_longueur", [[0, 0, 3, 1, 0, 4, 0, 5, 0, 4, 0, 3, 0, 4, 0, 0, 0, 5, 0]])
def test_reconstruction_codes_huffman(list_longueur):
    result = deflate.reconstruction_codes_huffman(list_longueur)

    list_resultat = [len(bin(result[index]))-2 if index in result else 0 for index in range(19)]

    assert list_longueur == list_resultat



"""
@pytest.mark.parametrize("message", [s,t])
def test_lempelZiv(message):       
    r,_,root = deflate.deflateLZW(message)
    result = deflate.inflateLZW(r,root)
    assert message == result
"""


