"""Module implémentant l'algorithme Deflate et Inflate
Les sous-fonctions sont utilisés dans les fonctions deflate() et inflate()

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
#ORDRE_3ARBRE_INVERSE = [3, 17, 15, 13, 11, 9, 7, 5, 4, 6, 8, 10, 12, 14, 16, 18, 0, 1, 2]
  
def conversion_classes_compression(valeur: int,table: list[int]) -> (int,int,int):
    """ Fonction pour convertir les valeurs selon la table
        Renvoie (symbol, valeur extra bits, nombre extra bit)
    """
    for base,symbol,extra in table:
        if valeur>=base and valeur < base + 2**(extra):
            return (symbol,valeur-base,extra)
   
    raise Exception(str(valeur)+" n'est pas dans la table")

def conversion_classes_decompression(symbole_compress: int,table: list[int]) -> (int, int):
    """ Fonction pour convertir en valeur selon la table
        Renvoie base
    """
    for base,symbol,nb_extra_bits in table:
        if symbol == symbole_compress:
            return base,nb_extra_bits
    raise Exception(str(symbole_compress)+" n'est pas dans la table")

def compressionLZ77(uncompressed_data):
    """Fonction de compression Lempel-Ziv-1977
        Les distances utilisés dans DEFLATE vont jusqu'à 32768 octets et les longueurs jusqu'à 258 octets.
    """
    buffer_behind=32768
    buffer_ahead=258

    freq_map_litteral = [0 for i in range(285)]
    freq_map_distances = [0 for i in range(30)]

    def correspondance_max(fenetre_precedants, fenetre_suivants):
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
                decalage_max = len(fenetre_precedants)-index_f
        return decalage_max, longueur_max

    resultat = [uncompressed_data[0]]
    freq_map_litteral[uncompressed_data[0]] += 1 
    i = 1
    taille = len(uncompressed_data)
    while i < taille:        
        decalage,longueur = correspondance_max(uncompressed_data[max(0,i-buffer_behind):i],uncompressed_data[i:min(len(uncompressed_data),i+buffer_ahead)])
     
        if longueur >=3:
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
    #Fin de bloc
    resultat.append(256)
    freq_map_litteral[256] = 1 
    return resultat, freq_map_litteral, freq_map_distances

def decompressionLZ77(compressed_message):
    """Décompression des données encodées en LZ77 
    """
    message_initial = []
    for elt in compressed_message:
        if isinstance(elt,tuple):
            longueur = elt[0]
            distance = elt[1]
            message_initial.extend(message_initial[len(message_initial)-distance:len(message_initial)-distance+longueur])
        else:
            if elt == 256:
                return message_initial
            else:
                message_initial.append(elt)
    return message_initial

def conversion_longueurs_symboles(longueurs):
    """Conversion d'une liste de symboles entre 0 et 15 en liste plus courte ou les plages sont converties en symboles
            RFC 1951:
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
        Retourne une liste de symboles 0–18 + liste de bits supplémentaires
    """
    symbols = []
    extra_bits = []

    i = 0
    n = len(longueurs)

    while i < n:
        cur = longueurs[i]

        # compter la longueur du run
        run = 1
        while i + run < n and longueurs[i + run] == cur:
            run += 1
        i += run
        if cur == 0:
            # utiliser 17 ou 18
            while run >= 11:
                cnt = min(run, 138)
                symbols.append(18)
                extra_bits.append(bin(cnt - 11)[2:].zfill(7))
                run -= cnt

            if run >= 3:
                symbols.append(17)
                extra_bits.append(bin(run - 3)[2:].zfill(3))
                run = 0

            while run > 0:
                symbols.append(0)
                run -= 1

        else:
            # émettre la première valeur
            symbols.append(cur)
            run -= 1

            # utiliser 16 pour les répétitions
            while run >= 3:
                cnt = min(run, 6)
                symbols.append(16)
                extra_bits.append(bin(cnt - 3)[2:].zfill(3))
                run -= cnt

            while run > 0:
                symbols.append(cur)
                run -= 1

        
    return symbols, extra_bits

def inversion_conversion_symbole_longueurs(list_symbole : list[int],list_extras : list[int]) -> list[int]:
    """Fonction inverse de la fonction conversion_longueurs_symbole
    """
    result = []
    index_extra = 0
    for symbole in list_symbole:
      
        if symbole <= 15:            
            result.append(symbole)
            continue

        elif symbole == 16:
            nb_repet = int(list_extras[index_extra],2)+3
            result.extend([result[-1] for i in range(nb_repet)])

        elif symbole == 17:
            nb_repet = int(list_extras[index_extra],2)+3
            result.extend([0 for i in range(nb_repet)])

        elif symbole == 18:
            nb_repet = int(list_extras[index_extra],2)+11
            result.extend([0 for i in range(nb_repet)])

        else:
            raise Exception("Erreur décompression")
        index_extra +=1
    return result

def Hlen(liste: list[int]) -> int:
    """Renvoie le dernier indice non nul de la liste +1
    """
    for i in range(len(liste)-1,0,-1):
        if liste[i] != 0:
            return i +1
    return 0

def deflate_data(lz77_compressed_data, dico_litt, dico_dist):
    """Compresse l'information lz77_compressed_data avec les dictionnaires de code des littéraux-longueurs et des distances
        Renvoie les données compressés en bits
    """
    resultat = ""
    for c in lz77_compressed_data:
        if not isinstance(c,tuple):
            resultat += dico_litt[c]
        else:
            length = c[0]
            distance = c[1]

            resultat += dico_litt[length[0]]
            if length[2]>0:
                resultat += bin(length[1])[2:].zfill(length[2])

            resultat += dico_dist[distance[0]]
            if distance[2]>0:
                resultat += bin(distance[1])[2:].zfill(distance[2])
    return resultat

def inflate_data(binary_data, arbre_litt, arbre_dist, temp_max_lit, temp_max_dist):
    """Décompresse les données compressés sous forme de bits en données du type list LZ77 littéraux+longueurs,distances
        Renvoie la liste des littéraux avec les longueurs, distances
    """
    encoded = binary_data

    resultat_data = []

    while len(encoded)>0:
        symbole,index = arbre_litt.decode_next_symbol(encoded[:temp_max_lit+1])
     
        encoded = encoded[index:]

        if symbole < 256:
            resultat_data.append(symbole)
        elif symbole == 256:
            resultat_data.append(symbole)
            return resultat_data
        else:
            base,nb_extra_bits = conversion_classes_decompression(symbole,LENGTH_TABLE)
            valeur_extra = int("0"+encoded[:nb_extra_bits],2)
            encoded=encoded[nb_extra_bits:]
            longueur = base+valeur_extra

            symbole_dist,index = arbre_dist.decode_next_symbol(encoded[:temp_max_dist+1])
          
            encoded = encoded[index:]
       
            base,nb_extra_bits = conversion_classes_decompression(symbole_dist,DISTANCE_TABLE)
            valeur_extra = int("0"+encoded[:nb_extra_bits],2)
            encoded=encoded[nb_extra_bits:]
            distance = base+valeur_extra

            resultat_data.append((longueur,distance))

    raise Exception("Pas de symbole (256) de fin!")


def deflate(message: str):
    """Implémentation de l'algorithme Deflate
        Renvoie le code du message encodé avec Deflate
    """

    compressed_lz77, list_litt, list_distances = compressionLZ77(message)
  
    # Obtention des arbres d'encodage des littéraux-longueurs et des distances
    arbre_litt = huff.generate_tree_list(list_litt)  #Liste [0-285] des littéraux et des décalages
    arbre_distance = huff.generate_tree_list(list_distances) #Liste des longueurs

    dico_litt_temp = {}
    huff.set_binary_code(arbre_litt,'', dico_litt_temp)
    dico_litt = huff.huffman_canonique([len(dico_litt_temp[index]) if index in dico_litt_temp else 0 for index in range(285)])
    print("Dictionnaire des littéraux de l'arbre d'Huffman ",dico_litt)

    dico_distance_temp = {}
    huff.set_binary_code(arbre_distance,'', dico_distance_temp)
    dico_distance = huff.huffman_canonique([len(dico_distance_temp[index]) if index in dico_distance_temp else 0 for index in range(30)])
    print("Dictionnaire des distances de l'arbre d'Huffman ",dico_distance)

    #Encodage des données
    resultat = deflate_data(compressed_lz77,dico_litt, dico_distance)

 
    # Construction du troisième arbre d'Huffman pour encoder les deux premiers
    longueur_codes_arbres_litt = [len(dico_litt[index_c]) if index_c in dico_litt else 0 for index_c in range(256+len(LENGTH_TABLE))]
    longueur_codes_arbres_dist = [len(dico_distance[index_c]) if index_c in dico_distance else 0 for index_c in range(len(DISTANCE_TABLE))]
  
    HLIT = Hlen(longueur_codes_arbres_litt) 
    HDIST = Hlen(longueur_codes_arbres_dist) 


    print("litt",longueur_codes_arbres_litt[:HLIT])
    print("dist",longueur_codes_arbres_dist[:HDIST])
    symboles_longueurs, extra_longueurs = conversion_longueurs_symboles(longueur_codes_arbres_litt[:HLIT]+longueur_codes_arbres_dist[:HDIST])

    print("liste des symboles des longueurs des codes des litteraux-longueurs-distances", symboles_longueurs)
    print(extra_longueurs)

    dico_frequences_longueurs_codes_arbres = huff.freq_map(symboles_longueurs)
    arbres_encodage = huff.generate_tree(dico_frequences_longueurs_codes_arbres)
    dico_longueurs_temp = {}
    huff.set_binary_code(arbres_encodage,'', dico_longueurs_temp)
    list_longueur = [len(dico_longueurs_temp[index]) if index in dico_longueurs_temp else 0 for index in range(19)]
    dico_longueurs = huff.huffman_canonique(list_longueur)
    print("Dictionnaire des codes des longueurs des codes ",dico_longueurs)

    #Encodage des arbres
    result = ""
    index_extra = 0
    for i,c in enumerate(symboles_longueurs):
        result += dico_longueurs[c]
        if c > 15:
            result += extra_longueurs[index_extra]
            index_extra+=1
 
    #Encodage de l'arbre d'encodage 
    rearanged_longueurs_codes_arbres_longueurs = [list_longueur[index_c] for index_c in ORDRE_3ARBRE]
    print("rearanged",rearanged_longueurs_codes_arbres_longueurs)
    # HLIT, HDIST, HCLEN dernier indice non nul des listes

    HCLEN = Hlen(rearanged_longueurs_codes_arbres_longueurs) 
    #print("HLIT, HDIST, HCLEN:",HLIT, HDIST, HCLEN)
    
    HLIT = HLIT-257
    HDIST = HDIST-1
    res = ""
    res += bin(HLIT)[2:].zfill(5) + bin(HDIST)[2:].zfill(5) + bin(HCLEN-4)[2:].zfill(4)

    for i in range(HCLEN):
        res += bin(rearanged_longueurs_codes_arbres_longueurs[i])[2:].zfill(3)
  
    return res+result+resultat

def inflate(code):
    """ Réciproque de deflate
    """
    print("----------------INFLATE-------------")

    # Lecture de HLIT, HDIST, HCLEN
    HLIT = int(code[:5],2)+257
    HDIST = int(code[5:10],2)+1
    HCLEN = int(code[10:14],2)+4
    encode = code[14:]

    #Lecture du troisième arbre
    list_longueur_code_arbre_longueurs_codes = [0 for i in range(len(ORDRE_3ARBRE))]
    
    for i in range(HCLEN):
        list_longueur_code_arbre_longueurs_codes[ORDRE_3ARBRE[i]] = int(encode[3*i:3*i+3],2)
    dico_codes_longueurs = huff.huffman_canonique(list_longueur_code_arbre_longueurs_codes)
    arbre_longueurs = huff.recreate_tree_from_dict(dico_codes_longueurs)
    encoded1 = encode[3*(HCLEN):]

    print(encoded1[:7])


    print("Dictionnaire troisième arbre",dico_codes_longueurs)
    

    #Lectures des deux premiers arbres
    lengths = []
    temp_max = max(list_longueur_code_arbre_longueurs_codes)
    while len(lengths) < HDIST+HLIT:
        symbole,index = arbre_longueurs.decode_next_symbol(encoded1[:temp_max+1])
      
        encoded1 = encoded1[index:]

        if symbole <= 15:
            lengths.append(symbole)
        elif symbole == 16:
            nb_repet = int(encoded1[:2],2)+3
            encoded1 = encoded1[2:]
            lengths.extend([lengths[-1] for i in range(nb_repet)])
        elif symbole == 17:
            nb_repet = int(encoded1[:3],2)+3
            encoded1 = encoded1[3:]
            lengths.extend([0 for i in range(nb_repet)])

        elif symbole == 18:
            nb_repet = int(encoded1[:7],2)+11
            encoded1 = encoded1[7:]
            lengths.extend([0 for i in range(nb_repet)])
        else:
            raise Exception("Erreur décompression")


    print("data:",encoded1[:7])

    #Création des arbres
    litlen_lengths = lengths[:HLIT]
    dist_lengths = lengths[HLIT:HLIT+HDIST]
    litlen_dict = huff.huffman_canonique(litlen_lengths)
    dist_dict = huff.huffman_canonique(dist_lengths)
    litlen_tree = huff.recreate_tree_from_dict(litlen_dict)
    dist_tree = huff.recreate_tree_from_dict(dist_dict)
    temp_max_lit = max(litlen_lengths)
    temp_max_dist = max(dist_lengths)


    #Lecture des données
    resultat_data = decompressionLZ77(inflate_data(encoded1, litlen_tree, dist_tree, temp_max_lit, temp_max_dist))

    return resultat_data
