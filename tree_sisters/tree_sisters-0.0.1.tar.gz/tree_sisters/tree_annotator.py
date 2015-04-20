from tree2tax.tree2tax import TaxonomyFunctions

class TreeAnnotator:
    def full_taxonomy(self, tree, node, separator='; '):
        name = ''
        if node.is_tip():
            node = node.parent
        while node.parent:
            current_name = TaxonomyFunctions().taxonomy_from_node_name(node.name)
            if current_name:
                if name == '':
                    name = current_name
                else:
                    name = "%s%s%s" % (current_name, separator, name)
            node = node.parent
        return name
        
    def find_named_parent(self, tree, node):
        n = node.parent
        while n is not None:
            name = TaxonomyFunctions().taxonomy_from_node_name(n.name)
            if name is not None:
                return n
            else:
                n = n.parent
        return None
    
    def find_sisters(self, tree, node):
        '''return a list of nodes that are named sister lineage LCAs (may be 0, 1 or more nodes that fit this description)'''
        
        stack = Stack() # collection of nodes that may contain sister lineages
        sisters = []
        n = node
        if n is None: return sisters
        visited_nodes = set([n])
        limited_by_parent = False
        
        while len(sisters) == 0 and n is not None:
            try:
                parent = n
                while True:
                    name = TaxonomyFunctions().taxonomy_from_node_name(n.name)
                    if name is not None and parent != n and not n.is_tip():
                        # this node is a sister
                        sisters.append(n)
                    else:
                        # not named, descend further
                        for d in n.children:
                            if d not in visited_nodes:
                                visited_nodes.add(d)
                                stack.push(d)
                    n = stack.pop()
            except IndexError: #stack is empty
                if limited_by_parent:
                    break
                # no sisters found at this level, go up one and try again
                n = n.parent
                visited_nodes.add(n)
                # if the new parent node is named, then we've reached the limit,
                # don't go any further
                if TaxonomyFunctions().taxonomy_from_node_name(n.name):
                    limited_by_parent = True
              
        if len(sisters) == 1 and sisters[0] == self.find_named_parent(tree, node):
            # Don't return a parent as a sister
            return []
        else: 
            return sisters
            
class Stack:
    def __init__(self):
        self.__storage = []

    def isEmpty(self):
        return len(self.__storage) == 0

    def push(self,p):
        self.__storage.append(p)

    def pop(self):
        return self.__storage.pop()