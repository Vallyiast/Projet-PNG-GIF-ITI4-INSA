class HuffmanNode:
    def __init__(self, freq=None, data=None, left=None, right=None):
        self.freq = freq
        self.data = data
        self.left = left
        self.right = right

    def toString(self) -> str:
        a,b,c,d="","","",""
        if self.left is not None:
            a = "l="+self.left.toString()
        if self.right is not None:
            b = ", r="+self.right.toString()
        if self.data is not None:
           c = str(self.data)
        return "HN( "+c+a+b+")"

    def freq_map(message) -> dict:    
        dico = {}
        for c in message:
            if c in dico:
                dico[c] += 1
            else:
                dico[c] = 1
        return dico

    def generate_tree(freq_map: dict):

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

    def generate_tree_list(freq_list : list):
        """Generate tree from list 
        """

        list_nodes = {}
        for index,c in enumerate(freq_list):
            if freq_list[index]>0:
                list_nodes[HuffmanNode(freq_list[index],index)] = freq_list[index]
        

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

    def set_binary_code(node, prefix: str, mapping: dict):
        if node.left ==None and node.right ==None: 
            mapping[node.data] = prefix    
        else:             
            HuffmanNode.set_binary_code(node.left, prefix+'0', mapping)
            HuffmanNode.set_binary_code(node.right, prefix+'1',mapping)

    def recreate_tree_from_dict(dictionnaire : dict):
        root = HuffmanNode()
        for key, value in dictionnaire.items():
            node = root

            for bit in value:
                if bit == '0':
                    if node.left is None:
                        node.left = HuffmanNode()
                    node = node.left
                else:
                    if node.right is None:
                        node.right = HuffmanNode()
                    node = node.right
            node.data = key
        return root

    def decode_next_symbol(self,tampon):
        node = self
        i = 0
        while node.data is None:
            bit = tampon[i]
            if bit == '0':
                node = node.left
            else:
                node = node.right  
            i +=1
             
        return node.data, i

    def huffman_canonique(list_longueur : list):
        """Reconstruit le dictionnaire des codes de l'arbre d'Huffman avec la longueur des codes de chaque symbole par Huffman canonique
            Renvoie la liste des codes pour les symboles d'indice i de [1,n] dans cet ordre
        """
        result = dict()

        bl_count = HuffmanNode.freq_map(list_longueur) #Compte le nombre de code de même longueur pour chaque longueur

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
dico = {0: '0', 1: '11110', 3: '1100', 4: '100', 5: '1101', 6: '11111', 7: '1110', 18: '101'}

root=HuffmanNode.recreate_tree_from_dict(dico)
#print(root.toString())
print(root.decode_next_symbol("11110011"))
"""
"""
result = huffman_canonique([0, 0, 3, 1, 0, 4, 0, 5, 0, 4, 0, 3, 0, 4, 0, 0, 0, 5, 0])
print(result)
"""