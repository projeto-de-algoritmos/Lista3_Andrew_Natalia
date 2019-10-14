class HeapNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class Heap:
    def __init__(self):
        self.nodes = [HeapNode('0', 0)]
        self.limit = 0

    def root(self):
        if(self.limit > 0):
            return self.nodes[1]
        else:
            return None

    def father(self, i):
        return round(i/2)
    
    def left(self, i):
        return 2 * i

    def right(self, i):
        return (2 * i) + 1

    def swap(self, i, j):
        aux = self.nodes[i]
        self.nodes[i] = self.nodes[j]
        self.nodes[j] = aux
    
    def heapify(self, i):
        if(self.limit <= 1):
            return

        l = self.left(i)
        r = self.right(i)

        if(l <= self.limit and self.nodes[l].value < self.nodes[i].value):
            smaller = l
        else:
            smaller = i

        if(r <= self.limit and self.nodes[r].value < self.nodes[smaller].value):
            smaller = r

        if(smaller != i):
            self.swap(i, smaller)
            self.heapify(smaller)


    def shift_up(self, i):
        f = self.father(i)

        if(f > 0 and self.nodes[i].value < self.nodes[f].value):
            self.swap(i, f)
            self.shift_up(f)

    def add(self, node):
        self.nodes.append(node)
        self.limit += 1
        self.shift_up(self.limit)

    def remove(self):
        node = None
        if(self.limit > 0):
            if(self.limit > 1):
                self.swap(1, self.limit)
            
            node = self.nodes.pop()
            self.limit -= 1
            self.heapify(1)

        return node


class HuffmanCoding:

    def __init__(self, word):
        self.word = word
        self.frequency = {}
        self.heap = Heap()
        self.codes = {}
        self.reverse_codes = {}
    
    def count_frequency(self):
        for char in self.word:
            if not char in self.frequency:
                self.frequency[char] = 0
            self.frequency[char] += 1

    def build_heap(self):
        for char in self.frequency:
            node = HeapNode(char, self.frequency[char])
            self.heap.add(node)

    def merge_nodes(self):
        while(self.heap.limit > 1):
            node1 = self.heap.remove()
            node2 = self.heap.remove()

            merged = HeapNode(None, node1.value + node2.value)
            merged.left = node1
            merged.right = node2

            self.heap.add(merged)

    def set_codes_util(self, node, code):
        if(node is None):
            return
        
        if(node.key is not None):
            self.codes[node.key] = code
            self.reverse_codes[code] = node.key
            return

        self.set_codes_util(node.left, code + "0")
        self.set_codes_util(node.right, code + "1")

    def set_codes(self):
        self.set_codes_util(self.heap.root(), "")

    def test(self):
        self.count_frequency()
        self.build_heap()
        self.merge_nodes()
        self.set_codes()

        # for i in range(self.heap.limit + 1):
        #     print(self.heap.nodes[i].key + str(self.heap.nodes[i].value))


if __name__ == "__main__":
    test = HuffmanCoding("teste")
    test.test()
    
