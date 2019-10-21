import igraph
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go

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

class TreePlot:

    def __init__(self, tree, encoded_text):
        self.tree = tree
        self.encoded_text = encoded_text
        self.nodes_quantity = 0
        self.labels = ""

        self.set_nodes_quantity()
        self.set_labels()
        self.set_tree()
        self.set_figure()
        self.plot_figure()

    def get_height(self, node):
        if node is None:
            return 0

        return max(self.get_height(node.left), self.get_height(node.right)) + 1

    def set_nodes_quantity(self):
        self.height = self.get_height(self.tree)
        self.nodes_quantity = (2 ** self.height) - 1

    def set_labels(self):
        queue = [self.tree]
        while len(queue) > 0:
            node = queue.pop(0)

            if(len(self.labels) < self.nodes_quantity):
                if(node == None):
                    self.labels += " "
                elif(node.key == "DAD"):
                    self.labels += "+"
                else:
                    if(node.key == ' '):
                        self.labels += "_"
                    else:
                        self.labels += node.key

                if(node == None):
                    queue.append(None)
                    queue.append(None)
                else:
                    queue.append(node.left)
                    queue.append(node.right)

    def set_tree(self):
        G = Graph.Tree(self.nodes_quantity, 2) # 2 stands for children number
        lay = G.layout('rt',  root=(0,0))

        self.position = {k: lay[k] for k in range(self.nodes_quantity)}
        self.Y = [lay[k][1] for k in range(self.nodes_quantity)]
        self.M = max(self.Y)

        es = EdgeSeq(G) # sequence of edges
        E = [e.tuple for e in G.es] # list of edges

        L = len(self.position)
        self.Xn = [self.position[k][0] for k in range(L)]
        self.Yn = [2*self.M-self.position[k][1] for k in range(L)]
        self.Xe = []
        self.Ye = []
        for edge in E:
            self.Xe+=[self.position[edge[0]][0],self.position[edge[1]][0], None]
            self.Ye+=[2*self.M-self.position[edge[0]][1],2*self.M-self.position[edge[1]][1], None]

    def set_figure(self):
        self.fig = go.Figure()
        self.fig.add_trace(go.Scatter(x=self.Xe,
                        y=self.Ye,
                        mode='lines',
                        line=dict(color='rgb(210,210,210)', width=1),
                        hoverinfo='none'
                        ))
        self.fig.add_trace(go.Scatter(x=self.Xn,
                        y=self.Yn,
                        mode='markers',
                        name='bla',
                        marker=dict(symbol='circle-dot',
                                        size=18, 
                                        color='#6175c1',    #'#DB4551', 
                                        line=dict(color='rgb(50,50,50)', width=1)
                                        ),
                        text=self.labels,
                        hoverinfo='text',
                        opacity=0.8
                        ))

    def make_annotations(self, pos, text, font_size=10, font_color='rgb(250,250,250)'):
        L=len(pos)
        if len(text)!=L:
            raise ValueError('The lists pos and text must have the same len')
        annotations = []
        for k in range(L):
            annotations.append(
                dict(
                    text=self.labels[k], # or replace labels with a different list for the text within the circle  
                    x=pos[k][0], y=2*self.M-self.position[k][1],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False)
            )
        return annotations

    def plot_figure(self):
        axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            )

        self.fig.update_layout(
            title=self.encoded_text,
            annotations=self.make_annotations(self.position, self.labels),
            font_size=12,
            showlegend=False,
            xaxis=axis,
            yaxis=axis,          
            margin=dict(l=40, r=40, b=85, t=100),
            hovermode='closest',
            plot_bgcolor='rgb(248,248,248)'          
        )
        self.fig.show()


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

            merged = HeapNode("DAD", node1.value + node2.value)
            merged.left = node1
            merged.right = node2

            self.heap.add(merged)

    def set_codes(self, node, code):
        if(node is None):
            return
        
        if(node.key != "DAD"):
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
            
            if(node.key != "DAD"):
                print(node.key)
                node = self.heap.root()


if __name__ == "__main__":
    # text = "Ana amam sua nana, sua mana e banana"
    # text = "teste"

    text = input("Insira uma palavra para ser codificada: ")

    hc = HuffmanCoding(text)
    
    hc.encode()

    print("\nDECODIFICANDO:\n")
    hc.decode()
    print("\nDECODIFICAÇÃO CONCLUÍDA\n")


    print("Veja a árvore de codificação e o código de huffman da palavra inserida!\n\n")
    TreePlot(hc.heap.root(), hc.encoded_text)
    
