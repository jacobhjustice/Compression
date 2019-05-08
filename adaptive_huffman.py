import copy
import math

class Letter:
    def __init__(self, letter, ascii_value, count):
        self.letter = letter
        self.ascii = ascii_value
        self.count = count
        self.parent = None

    def increment_count(self):
        self.count = self.count + 1

    def get_count(self):
        return self.count

    def get_ascii(self):
        return self.ascii

    def type(self):
        return "Leaf"

    def attach_parent(self, parent):
        self.parent = parent

# Nodes are objects used inside of the binary tree built within the Huffman_Tree class. 
# Nodes are recursive in nature; children of the node will either be other nodes, or letters (in the case where the child is a leaf).
# In encoding, childA is assigned to the smaller order of the nodes/letters.
# In decoding, a "0" in the code stream is represented by taking childA, a "1" represents taking childB
class Node:
    def __init__(self, childA, childB):
        self.childA = childA
        self.childB = childB

    def get_count(self):
        return self.childA.get_count() + self.childB.get_count()

    def get_ascii(self):
        asciiA = self.childA.get_ascii()
        asciiB = self.childB.get_ascii()
        return asciiA if asciiA > asciiB else asciiB

    def type(self):
        return "Node"

    def attach_parent(self, parent):
        self.parent = parent

class Heap:
    def __init__(self, leaves):
        self.leaves = []
        while len(leaves) > 1:
                # Smallest letter
            minA = Letter(None, 999, 999)
            # Second smallest letter
            minB = Letter(None, 999, 999)

            for letter in leaves:
                if letter.get_count() < minA.get_count() or (letter.get_count() == minA.get_count() and letter.get_ascii() < minA.get_ascii()):
                    minB = minA
                    minA = letter
                elif letter.get_count() < minB.get_count() or (letter.get_count() == minB.get_count() and letter.get_ascii() < minB.get_ascii()):
                    minB = letter
            node = Node(minA, minB)
            leaves.remove(minA)
            index = leaves.index(minB)
            leaves[index] = node
            minA.attach_parent(node)
            minB.attach_parent(node)
            if minA.type() == "Leaf":
                self.leaves.append(minA)
            if minB.type() == "Leaf":
                self.leaves.append(minB)
        self.root = leaves[0]
        


class Huffman:
    valid_characters = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

    # letters serves as an array of letters that will become the leaves of the heap when build is called
    def __init__(self):
        self.letters = []
        for i in range(len(self.valid_characters)):
            char = self.valid_characters[i]
            self.letters.append(Letter(char, 32 + i, 1))
        self.last_build = []

    # build returns a tree of Nodes used to decode text.
    def build_heap(self):
        arr = copy.deepcopy(self.letters)
        return Heap(arr)

    def increment_count_by_ascii(self, ascii):
        low = 0
        high = len(self.letters) - 1

        while low != high:
            index = int((low + high) / 2)
            if ascii > self.letters[index].ascii:
                low = index
            elif ascii < self.letters[index].ascii:
                high = index
            else:
                self.letters[index].increment_count()
                return True
        return False

    def adaptive_huffman_encode(self, str):
        code = ""
        while len(str) > 0:
            encoding = ""
            self.build_heap()
            #traverse parent
            #build up encoding as you go up
            #reverse encoding
            #append to code
        #print code at end
            
    def adaptive_huffman_decode(self, str):
        source_text = ""
        while len(str) > 0:
            heap = self.build_heap()
            node = heap.root
            while node.type() == "Node":
                code = str[0:1]
                str = str[1:]

                if code == "1":
                    node = node.childB
                elif code == "0":
                    node = node.childA
                else:
                    print("ERROR: RAN OUT OF DECODE")
                    return 0         
            # End stream for this letter, move on to next
            source_text = source_text + chr(node.ascii)
            success = self.increment_count_by_ascii(node.ascii)
            if success == False:
                print("ERROR: FAILED TO FIND ASCII")
                exit            

        print(source_text)



tree = Huffman()
tree.adaptive_huffman_decode("11010001101000")
