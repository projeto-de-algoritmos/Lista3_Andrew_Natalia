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

        if(self.limit > 0):
            self.shift_up(self.limit + 1)

        self.limit += 1

    def remove(self):
        node = None
        if(self.limit > 0):
            node = self.nodes[self.limit]

            if(self.limit > 1):
                self.swap(1, self.limit)
                self.heapify(1)

            self.limit -= 1

        return node


class HuffmanCoding:

    def __init__(self, word):
        self.word = word
        self.frequency = {}
        self.heap = Heap()
        self.codes = {}
    
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

            value1 = 0
            value2 = 0

            if(node1 is not None):
                value1 = node1.value
            if(node2 is not None):
                value2 = node2.value

            merged = HeapNode('+', value1 + value2)
            merged.left = node1
            merged.right = node2

            self.heap.add(merged)

            print(self.heap.nodes[self.heap.limit].value)

    def test(self):
        self.count_frequency()
        self.build_heap()
        self.merge_nodes()
        # for i in range(self.heap.limit + 1):
        #     print(self.heap.nodes[i].value)


if __name__ == "__main__":
    test = HuffmanCoding("banana")
    test.test()
    
