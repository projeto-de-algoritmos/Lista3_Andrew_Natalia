class HeapNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class Heap:
    def __init__(self):
        self.nodes = [HeapNode(None, 0)]

    def root(self):
        if(len(self.nodes) > 1):
            return self.nodes[1]
        else:
            return None

    def father(self, i):
        return i//2
    
    def left(self, i):
        return 2 * i

    def right(self, i):
        return (2 * i) + 1

    def swap(self, i, j):
        aux = self.nodes[i]
        self.nodes[i] = self.nodes[j]
        self.nodes[j] = aux
    
    def heapify(self, i):
        if(len(self.nodes) <= 2):
            return

        l = self.left(i)
        r = self.right(i)

        if(l < len(self.nodes) and self.nodes[l].value < self.nodes[i].value):
            smaller = l
        else:
            smaller = i

        if(r < len(self.nodes) and self.nodes[r].value < self.nodes[smaller].value):
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
        self.shift_up(len(self.nodes) - 1)

    def remove(self):
        node = None
        if(len(self.nodes) > 0):
            if(len(self.nodes) > 1):
                self.swap(1, len(self.nodes) - 1)
            
            node = self.nodes.pop()
            self.heapify(1)

        return node


class HuffmanCoding:

    def __init__(self, text):
        self.text = text
        self.frequency = {}
        self.heap = Heap()
        self.codes = {}
        self.encoded_text = ""
    
    def count_frequency(self):
        for char in self.text:
            if not char in self.frequency:
                self.frequency[char] = 0
            self.frequency[char] += 1

    def build_heap(self):
        for char in self.frequency:
            node = HeapNode(char, self.frequency[char])
            self.heap.add(node)

    def merge_nodes(self):
        while(len(self.heap.nodes) > 2):
            node1 = self.heap.remove()
            node2 = self.heap.remove()

            merged = HeapNode(None, node1.value + node2.value)
            merged.left = node1
            merged.right = node2

            self.heap.add(merged)

    def set_codes(self, node, code):
        if(node is None):
            return
        
        if(node.key is not None):
            self.codes[node.key] = code
            return

        self.set_codes(node.left, code + "0")
        self.set_codes(node.right, code + "1")

    def encode(self):
        self.count_frequency()
        self.build_heap()
        self.merge_nodes()
        self.set_codes(self.heap.root(), "")

        for char in self.text:
            self.encoded_text += self.codes[char]

    def decode(self):
        node = self.heap.root()

        for char in self.encoded_text:
            if(char == '0'):
                node = node.left
            elif(char == '1'):
                node = node.right
            
            if(node.key is not None):
                print(node.key)
                node = self.heap.root()


    # def print_heap(self):
    #     key = "dad"
    #     for node in self.heap.nodes:
    #         if(node.key is not None):
    #             key = node.key
    #         print(key + "-" + str(node.value))


if __name__ == "__main__":
    test = HuffmanCoding("teste")
    test.encode()

    print(test.encoded_text)

    test.decode()
    
