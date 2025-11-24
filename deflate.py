from huffman_node import HuffmanNode as huff
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


DISTANCE_TABLE = [
    # (premier nombre de la classe, symbole, nombre de bits supplémentaires)
    (1,0,0),
    (2,1,0),
    (3,2,0),
    (4,3,0),
    (5,4,1),
    (7,5,1),
    (9,6,2),
    (13,7,2),
    (17,8,3),
    (25,9,3),
    (33,10,4),
    (49,11,4),
    (65,12,5),
    (97,13,5),
    (129,14,6),
    (193,15,6),
    (257,16,7),
    (385,17,7),
    (513,18,8),
    (769,19,8),
    (1025,20,9),
    (1537,21,9),
    (2049,22,10),
    (3073,23,10),
    (4097,24,11),
    (6145,25,11),
    (8193,26,12),
    (12289,27,12),
    (16385,28,13),
    (24577,29,13)
]
LENGTH_TABLE = [
    # (premier nombre de la classe, symbole, nombre de bits supplémentaires)
    (3,257,0),
    (4,258,0),
    (5,259,0),
    (6,260,0),
    (7,261,0),
    (8,262,0),
    (9,263,0),
    (10,264,0),
    (11,265,1),
    (13,266,1),
    (15,267,1),
    (17,268,1),
    (19,269,2),
    (23,270,2),
    (27,271,2),
    (31,272,2),
    (35,273,3),
    (43,274,3),
    (51,275,3),
    (59,276,3),
    (67,277,4),
    (83,278,4),
    (99,279,4),
    (115,280,4),
    (131,281,5),
    (163,282,5),
    (195,283,5),
    (227,284,5)
]

ORDRE_3ARBRE = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]
  
def conversion_classes(valeur,table):
    """ Fonction pour convertir les valeurs selon la table
    """
    for base,symbol,extra in table:
        if valeur>=base and valeur < base + 2**(extra):
            return (symbol,valeur-base,extra)


def compressionLZ77(uncompressed_data):
    """Fonction de compression Lempel-Ziv-1977
        Les distances utilisés dans DEFLATE vont jusqu'à 32768 octets et les longueurs jusqu'à 258 octets.
    """
    buffer_behind=32768
    buffer_ahead=258

    freq_map_litteral = [0 for i in range(285)]
    freq_map_distances = [0 for i in range(30)]

    def correspondance_max(fenetre_precedants, fenetre_suivants,position):
        """
        """
        decalage_max = 0
        longueur_max = 0
        for index_f in range(len(fenetre_precedants)):
            longueur = 0
            while fenetre_precedants[index_f+longueur] == fenetre_suivants[longueur]:

                longueur+=1
                if longueur>=len(fenetre_suivants) or longueur+index_f>=len(fenetre_precedants):
                   
                    break 
        
            if longueur>longueur_max:
                longueur_max = longueur
                decalage_max = position-index_f
        return decalage_max, longueur_max

    resultat = [uncompressed_data[0]]
    i = 1
    taille = len(uncompressed_data)

    while i < taille:        
        decalage,longueur = correspondance_max(uncompressed_data[max(0,i-buffer_behind):i],uncompressed_data[i:min(len(uncompressed_data),i+buffer_ahead)],i)
     
        if longueur >3:
            r1 = conversion_classes(longueur,LENGTH_TABLE)
            r2 = conversion_classes(decalage,DISTANCE_TABLE)
         
            freq_map_litteral[r1[0]] += 1 
            freq_map_distances[r2[0]] += 1 

            resultat.append((r1,r2))
            i += longueur
        else:
            resultat.append(uncompressed_data[i])
            freq_map_litteral[ord(uncompressed_data[i])] += 1 
            i+=1        
    return resultat, freq_map_litteral, freq_map_distances


s = "code code code code"
t = "lorem ipsum versi color colem ispum veri color"
lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit."
resultLZ77 = compressionLZ77(t)

def conversion_longueurs_symboles(list_longueurs):
    """ Conversion des longueurs selon le RFC 1951:
            0 - 15: Represent code lengths of 0 - 15
            16: Copy the previous code length 3 - 6 times.
                The next 2 bits indicate repeat length
                        (0 = 3, ... , 3 = 6)
                    Example:  Codes 8, 16 (+2 bits 11),
                            16 (+2 bits 10) will expand to
                            12 code lengths of 8 (1 + 6 + 5)
            17: Repeat a code length of 0 for 3 - 10 times.
                (3 bits of length)
            18: Repeat a code length of 0 for 11 - 138 times
                (7 bits of length)
    """
    result = []
    list_extra = [] #Liste des bits supplémentaires 

    predecesseur = 16
    nb_predecesseur = 0

    for index_l, l in enumerate(list_longueurs):
        if predecesseur == l:
            nb_predecesseur +=1
        else:
            if predecesseur == 0:
                nb_18_full = nb_predecesseur//138 #Nombre de répétitions de 0 de plus de 138 fois
                reste_18_full = nb_predecesseur%138
                for nb in range(nb_18_full):
                    result.append(18)
                    list_extra.append(127)
                if reste_18_full>9:
                    result.append(18)
                    list_extra.append(reste_18_full)
                elif reste_18_full>2:              
                    result.append(17)
                    list_extra.append(reste_18_full)
                else:
                    result.extend([0 for i in range(reste_18_full)])


            else:
                nb_16_full = nb_predecesseur//6 #Nombre de répétitions du symbole de plus de 6 fois
                reste_16_full = nb_predecesseur%6
                for nb in range(nb_16_full):
                    result.append(16)
                    list_extra.append(3)
                if reste_16_full>2:
                    result.append(16)
                    list_extra.append(reste_16_full)
                else:
                    result.extend([7 for i in range(reste_16_full)])


            result.append(l)
            predecesseur = l
            nb_predecesseur = 0

    return result, list_extra



def deflate(message: str):
    resultat = ""

    compressed_lz77, list_litt, list_distances = compressionLZ77(message)
    print(compressed_lz77)


    # Obtention des arbres d'encodage des littéraux-longueurs et des distances
    arbre_litt = huff.generate_tree_list(list_litt)  #Liste [0-285] des littéraux et des décalages
    arbre_distance = huff.generate_tree_list(list_distances) #Liste des longueurs

    dico_litt = {}
    huff.set_binary_code(arbre_litt,'', dico_litt)
    print("Dictionnaire des littéraux de l'arbre d'Huffman ",dico_litt)

    dico_distance = {}
    huff.set_binary_code(arbre_distance,'', dico_distance)
    print("Dictionnaire des distances de l'arbre d'Huffman ",dico_distance)

    #Encodage des données

    for c in compressed_lz77:
        if isinstance(c,str):
            resultat += dico_litt[ord(c)]
        else:
            length = c[0]
            distance = c[1]

            resultat += dico_litt[length[0]]
            if length[2]>0:
                resultat += bin(length[1])[2:]

            resultat += dico_distance[distance[0]]
            if distance[2]>0:
                resultat += bin(distance[1])[2:]

    print("Resultat intermédiaire ",resultat)
            

    # Construction du troisième arbre d'Huffman pour encoder les deux premiers
    longueur_codes_arbres_litt = [len(dico_litt[index_c]) if index_c in dico_litt else 0 for index_c in range(256+len(LENGTH_TABLE))]
    longueur_codes_arbres_dist = [len(dico_distance[index_c]) if index_c in dico_distance else 0 for index_c in range(len(DISTANCE_TABLE))]
    
    symboles_longueurs, extra_longueurs = conversion_longueurs_symboles(longueur_codes_arbres_litt+longueur_codes_arbres_dist)
    print("liste des symboles des longueurs", symboles_longueurs)
    print(extra_longueurs)

    dico_frequences_longueurs_codes_arbres = huff.freq_map(symboles_longueurs)
    arbres_encodage = huff.generate_tree(dico_frequences_longueurs_codes_arbres)

    dico_longueurs = {}
    huff.set_binary_code(arbres_encodage,'', dico_longueurs)
    print("Dictionnaire des codes des longueurs des codes ",dico_longueurs)

    #Encodage des arbres
    result = ""
    index_extra = 0
    for i,c in enumerate(symboles_longueurs):
        result += dico_longueurs[c]
        if c > 15:
            result += bin(extra_longueurs[index_extra])[2:]
            index_extra+=1
    print(result)

    #Encodage de l'arbre d'encodage 
    print("Litt",longueur_codes_arbres_litt)
    print("Distance",longueur_codes_arbres_dist)
    longueurs_codes_arbre_longueurs = [len(dico_longueurs[index_c]) if index_c in dico_longueurs else 0 for index_c in range(19)]
    
    print("Longueurs",longueurs_codes_arbre_longueurs)
    rearanged_longueurs_codes_arbres_longueurs = [len(dico_longueurs[index_c]) if index_c in dico_longueurs else 0 for index_c in ORDRE_3ARBRE]
    print(rearanged_longueurs_codes_arbres_longueurs)

    HLIT = sum([1 if index_c in dico_litt else 0 for index_c in range(256+len(LENGTH_TABLE))])
    HDIST = sum([1 if index_c in dico_distance else 0 for index_c in range(len(DISTANCE_TABLE))])
    HCLEN = sum([1 if index_c in dico_longueurs else 0 for index_c in ORDRE_3ARBRE])


    return result+resultat

deflate(t)








def deflateLZW(message: str) -> tuple[str, dict, huff]:
    """Deflate algorithme utilisant compression LZW + Huffman
    """

    codeLZ, dicoLZ = lempelziv(message)
    print("Code par Lempel-Ziv",codeLZ)

    dico = {}
    frequences = huff.freq_map(codeLZ)
    print("Dico de fréquences ",frequences)
    arbre = huff.generate_tree(frequences)
    huff.set_binary_code(arbre,'', dico)
    print("Dictionnaire de l'arbre d'Huffman ",dico)

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


"""
r,_,root = deflateLZW(s)
print(r)
print(inflateLZW(r,root))
"""

