"""Module implémentant l'algorithme Deflate 
"""

from huffman_node import HuffmanNode as huff

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
ORDRE_3ARBRE_INVERSE = [3, 17, 15, 13, 11, 9, 7, 5, 4, 6, 8, 10, 12, 14, 16, 18, 0, 1, 2]
  
def conversion_classes_compression(valeur,table):
    """ Fonction pour convertir les valeurs selon la table
        Renvoie (symbol, valeur extra bits, nombre extra bit)
    """
    for base,symbol,extra in table:
        if valeur>=base and valeur < base + 2**(extra):
            return (symbol,valeur-base,extra)
    raise Exception(valeur+" n'est pas dans la table")

def conversion_classes_decompression(symbole_compress,table):
    """ Fonction pour convertir en valeur selon la table
        Renvoie base
    """
    for base,symbol,_ in table:
        if symbol == symbole_compress:
            return base
    raise Exception(symbole_compress+" n'est pas dans la table")


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
    freq_map_litteral[uncompressed_data[0]] += 1 
    i = 1
    taille = len(uncompressed_data)

    while i < taille:        
        decalage,longueur = correspondance_max(uncompressed_data[max(0,i-buffer_behind):i],uncompressed_data[i:min(len(uncompressed_data),i+buffer_ahead)],i)
     
        if longueur >3:
            r1 = conversion_classes_compression(longueur,LENGTH_TABLE)
            r2 = conversion_classes_compression(decalage,DISTANCE_TABLE)
         
            freq_map_litteral[r1[0]] += 1 
            freq_map_distances[r2[0]] += 1 

            resultat.append((r1,r2))
            i += longueur
        else:
            resultat.append(uncompressed_data[i])
            freq_map_litteral[uncompressed_data[i]] += 1 
            i+=1   

    return resultat, freq_map_litteral, freq_map_distances

def decompressionLZ77(compressed_message):
    """Décompression des données encodées en LZ77 
    """

    message_initial = []
    for elt in compressed_message:
        if isinstance(elt,tuple):
            longueur = conversion_classes_decompression(elt[0][0],LENGTH_TABLE)+elt[0][1]
            distance = conversion_classes_decompression(elt[1][0],DISTANCE_TABLE)+elt[1][1]
            message_initial.extend(message_initial[len(message_initial)-distance:len(message_initial)-distance+longueur])
        else:
            message_initial.append(elt)
    return message_initial


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

    for l in list_longueurs:
        if predecesseur == l:
            nb_predecesseur +=1
        else:
            if predecesseur == 0:
                nb_18_full = nb_predecesseur//138 #Nombre de répétitions de 0 de plus de 138 fois
                reste_18_full = nb_predecesseur%138
                for _ in range(nb_18_full):
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
                for _ in range(nb_16_full):
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

def Hlen(liste):
    """Renvoie le dernier indice non nul de la liste 
    """
    for i in range(len(liste)-1,0,-1):
        if liste[i] != 0:
            return i 
    return 0
   
def deflate(message: str):
    """Implémentation de l'algorithme Deflate
        Renvoie le code du message encodé avec Deflate
    """
    resultat = ""

    compressed_lz77, list_litt, list_distances = compressionLZ77(message)
 
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
        if not isinstance(c,tuple):
            resultat += dico_litt[c]
        else:
            length = c[0]
            distance = c[1]

            resultat += dico_litt[length[0]]
            if length[2]>0:
                resultat += bin(length[1])[2:]

            resultat += dico_distance[distance[0]]
            if distance[2]>0:
                resultat += bin(distance[1])[2:]

 

    # Construction du troisième arbre d'Huffman pour encoder les deux premiers
    longueur_codes_arbres_litt = [len(dico_litt[index_c]) if index_c in dico_litt else 0 for index_c in range(256+len(LENGTH_TABLE))]
    longueur_codes_arbres_dist = [len(dico_distance[index_c]) if index_c in dico_distance else 0 for index_c in range(len(DISTANCE_TABLE))]

    symboles_longueurs, extra_longueurs = conversion_longueurs_symboles(longueur_codes_arbres_litt+longueur_codes_arbres_dist)
    print("liste des symboles des longueurs", symboles_longueurs)
    print(extra_longueurs)

    dico_frequences_longueurs_codes_arbres = huff.freq_map(symboles_longueurs)
    arbres_encodage = huff.generate_tree(dico_frequences_longueurs_codes_arbres)

    dico_longueurs_temp = {}
    huff.set_binary_code(arbres_encodage,'', dico_longueurs_temp)
    list_longueur = [len(dico_longueurs_temp[index]) if index in dico_longueurs_temp else 0 for index in range(19)]
    print(list_longueur)
    dico_longueurs = huffman_canonique(list_longueur)
    print("Dictionnaire des codes des longueurs des codes ",dico_longueurs)

    #Encodage des arbres
    result = ""
    index_extra = 0
    for i,c in enumerate(symboles_longueurs):
        result += dico_longueurs[c]
        if c > 15:
            result += bin(extra_longueurs[index_extra])[2:]
            index_extra+=1
 
    #Encodage de l'arbre d'encodage 
    rearanged_longueurs_codes_arbres_longueurs = [list_longueur[index_c] for index_c in ORDRE_3ARBRE]
    print("rearanged",rearanged_longueurs_codes_arbres_longueurs)
    # HLIT, HDIST, HCLEN dernier indice non nul des listes
    HLIT = Hlen(longueur_codes_arbres_litt) - 256
    HDIST = Hlen(longueur_codes_arbres_dist) 
    HCLEN = Hlen(rearanged_longueurs_codes_arbres_longueurs) - 3
    #print("HLIT, HDIST, HCLEN:",HLIT, HDIST, HCLEN)

    res = ""
    res += bin(HLIT)[2:].zfill(5) + bin(HDIST)[2:].zfill(5) + bin(HCLEN)[2:].zfill(4)

    for i in range(HCLEN+4):
        res += bin(rearanged_longueurs_codes_arbres_longueurs[i])[2:].zfill(3)
  
    return res+result+resultat


def huffman_canonique(list_longueur):
    """Reconstruit le dictionnaire des codes de l'arbre d'Huffman avec la longueur des codes de chaque symbole par Huffman canonique
        Renvoie la liste des codes pour les symboles d'indice i de [1,n] dans cet ordre
    """
    result = dict()

    bl_count = huff.freq_map(list_longueur) #Compte le nombre de code de même longueur pour chaque longueur

    code = 0
    next_code = [0 for i in range(max(list_longueur)+1)]
    for bits in range(2,max(list_longueur)+1):
        if bits-1 in bl_count:
            code = (code+bl_count[bits-1])*2
        else:
            code = code*2
        next_code[bits] = code

    for n in range(len(list_longueur)):
        long = list_longueur[n]
        if (long != 0):
            result[n] = bin(next_code[long])[2:].zfill(long)
            next_code[long]+=1
   
    return result
"""
result = huffman_canonique([0, 0, 3, 1, 0, 4, 0, 5, 0, 4, 0, 3, 0, 4, 0, 0, 0, 5, 0])
print(result)
"""

def inflate(code):
    """ Réciproque de deflate
    """
    print("----------------INFLATE-------------")

    HLIT = int(code[:5],2)
    HDIST = int(code[5:10],2)
    HCLEN = int(code[10:14],2)

    encode = code[14:]

    #print("HLIT, HDIST, HCLEN:",HLIT, HDIST, HCLEN)

    list_longueur_code_arbre_longueurs_codes = [0 for i in range(len(ORDRE_3ARBRE))]
    
    for i in range(HCLEN+4):
        list_longueur_code_arbre_longueurs_codes[i] = int(encode[3*i:3*i+3],2)
    
    print("rearanged",list_longueur_code_arbre_longueurs_codes)
    list_longueur_code_arbre_longueurs_sorted = [list_longueur_code_arbre_longueurs_codes[ORDRE_3ARBRE_INVERSE[index]] for index in range(len(ORDRE_3ARBRE))]
    print(list_longueur_code_arbre_longueurs_sorted)
    dict_code_unsorted_longueurs = huffman_canonique(list_longueur_code_arbre_longueurs_sorted)
   
    print("codes longueurs",dict_code_unsorted_longueurs)

t = "lorem ipsum versi color colem ispum veri color"

code = deflate([ord(c) for c in t])

inflate(code)
