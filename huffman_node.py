class HuffmanNode:
    def __init__(self, freq, data, left=None, right=None):
        self.freq = freq
        self.data = data
        self.left = left
        self.right = right


    def freq_map(message) -> dict:    
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

    def generate_tree_list(freq_list):
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

    def set_binary_code(node, prefix, mapping):
        if node.left ==None and node.right ==None: 
            mapping[node.data] = prefix    
        else:             
            HuffmanNode.set_binary_code(node.left, prefix+'0', mapping)
            HuffmanNode.set_binary_code(node.right, prefix+'1',mapping)

    def encodage_hex():
        """ 
        """

