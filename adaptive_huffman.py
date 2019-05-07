import copy
import math

class Letter:
    def __init__(self, letter, ascii_value, count):
        self.letter = letter
        self.ascii = ascii_value
        self.count = count

    def increment_count(self):
        self.count = self.count + 1

    def get_count(self):
        return self.count

    def get_ascii(self):
        return self.ascii

    def type(self):
        return "Leaf"

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

class Huffman_Tree:
    valid_characters = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    

    # arr serves as an array of letters that will become the leaves of the tree when build is called
    def __init__(self):
        self.arr = []
        for i in range(len(self.valid_characters)):
            char = self.valid_characters[i]
            self.arr.append(Letter(char, 32 + i, 1))

    # build returns a tree of Nodes used to decode text.
    def build(self):
        arr = copy.deepcopy(self.arr)
        while len(arr) > 1:
            # Smallest letter
            minA = Letter(None, 999, 999)
            # Second smallest letter
            minB = Letter(None, 999, 999)

            for letter in arr:
                if letter.get_count() < minA.get_count() or (letter.get_count() == minA.get_count() and letter.get_ascii() < minA.get_ascii()):
                    minB = minA
                    minA = letter
                elif letter.get_count() < minB.get_count() or (letter.get_count() == minB.get_count() and letter.get_ascii() < minB.get_ascii()):
                    minB = letter
            node = Node(minA, minB)
            arr.remove(minA)
            index = arr.index(minB)
            arr[index] = node

        return arr[0]

    def increment_count_by_ascii(self, ascii):
        low = 0
        high = len(self.arr) - 1

        while low != high:
            index = int((low + high) / 2)
            if ascii > self.arr[index].ascii:
                low = index
            elif ascii < self.arr[index].ascii:
                high = index
            else:
                self.arr[index].increment_count()
                return True
        return False

    def adaptive_huffman_encode(self, str):
        for chr in str:
            ascii = ord(chr)
            
    def adaptive_huffman_decode(self, str):
        source_text = ""
        while len(str) > 0:
            node = self.build()
            while node.type() == "Node":
                code = str[0:1]
                str = str[1:]

                if code == "1":
                    node = node.childB
                elif code == "0":
                    node = node.childA
                else:
                    print("ERROR: RAN OUT OF DECODE")
                    return 0;            
            # End stream for this letter, move on to next
            source_text = source_text + chr(node.ascii)
            success = self.increment_count_by_ascii(node.ascii)
            if success == False:
                print("ERROR: FAILED TO FIND ASCII")
                exit            

        print(source_text)



tree = Huffman_Tree()
tree.adaptive_huffman_decode("11010001101000")
