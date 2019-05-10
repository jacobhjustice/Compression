import copy, sys, struct

#TODO Create parent class for letter and node for shared functions

class Node: 
    def __init__(self):
        self.parent = None

    # Required functions for subclass
    def get_count(self):
        return NotImplementedError

    def get_ascii(self):
        return NotImplementedError

    def type(self):
        return NotImplementedError


    # Shared functionality
    def attach_parent(self, parent):
        self.parent = parent

    def traverse_parent(self):
        if self.parent is None:
            return [None]
        node = self.parent
        if node.childA == self:
            return [node, "0"]
        if node.childB == self:
            return [node, "1"]
        print("ERROR: Parent attached does not reference the correct child")
        sys.exit()

class Letter(Node):
    def __init__(self, letter, ascii_value, count):
        self.letter = letter
        self.ascii = ascii_value
        self.count = count
        super().__init__()

    def increment_count(self):
        self.count = self.count + 1

    def get_count(self):
        return self.count

    def get_ascii(self):
        return self.ascii

    def type(self):
        return "Leaf"

# Parents are objects used inside of the binary tree built within the Huffman_Tree class. 
# Parents are recursive in nature; children of the parent will also be nodes: either be other parents, or letters (in the case where the child is a leaf).
# In encoding, childA is assigned to the smaller order of the nodes.
# In decoding, a "0" in the code stream is represented by taking childA, a "1" represents taking childB
class Parent(Node):
    def __init__(self, childA, childB):
        self.childA = childA
        self.childB = childB
        super().__init__()

    def get_count(self):
        return self.childA.get_count() + self.childB.get_count()

    def get_ascii(self):
        asciiA = self.childA.get_ascii()
        asciiB = self.childB.get_ascii()
        return asciiA if asciiA > asciiB else asciiB

    def type(self):
        return "Parent"

class Heap:
    def __init__(self, leaves):
        self.leaves = []
        for l in leaves:
            self.leaves.append(l)
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
            node = Parent(minA, minB)
            leaves.remove(minA)
            index = leaves.index(minB)
            leaves[index] = node
            minA.attach_parent(node)
            minB.attach_parent(node)
        self.root = leaves[0]

    def get_leaf_by_ascii(self, ascii):
        low = 0
        high = len(self.leaves) - 1
        while low != high:
            index = int((low + high + 1) / 2)
            if ascii > self.leaves[index].ascii:
                low = index 
            elif ascii < self.leaves[index].ascii:
                high = index 
            else:
                return self.leaves[index]
        return None
        


class Huffman:
    valid_characters = "  !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\b "

    # letters serves as an array of letters that will become the leaves of the heap when build is called
    def __init__(self):
        self.letters = []
        for i in range(len(self.valid_characters)):
            char = self.valid_characters[i]
            self.letters.append(Letter(char, 31 + i, 1))
        self.last_build = []

    # build returns a tree of Nodes used to decode text.
    def build_heap(self):
        arr = copy.deepcopy(self.letters)
        return Heap(arr)

    def increment_count_by_ascii(self, ascii):
        low = 0
        high = len(self.letters) - 1
        while low != high:
            index = int((low + high + 1) / 2)
            if ascii > self.letters[index].ascii:
                low = index
            elif ascii < self.letters[index].ascii:
                high = index
            else:
                self.letters[index].increment_count()
                return True
        return False

    def adaptive_huffman_encode(self, str):
        str = str + "\b"
        code = ""
        while len(str) > 0:
            encoding = ""
            chr = str[0:1]
            str = str[1:]
            ascii = ord(chr)
            if chr == "\b":
                ascii = 127
            heap = self.build_heap()
            leaf = heap.get_leaf_by_ascii(ascii)
            if leaf is None:
                print("ERROR: LEAF NOT FOUND")
                sys.exit()
            results = leaf.traverse_parent()
            while results[0] is not None:
                leaf = results[0]
                encoding = results[1] + encoding
                results = leaf.traverse_parent()
            code = code + encoding
            success = self.increment_count_by_ascii(ascii)
            if success == False:
                print("ERROR: FAILED TO FIND ASCII")
                sys.exit()       

        return code
        
    def adaptive_huffman_decode(self, str):
        source_text = ""
        while len(str) > 0:
            heap = self.build_heap()
            node = heap.root
            while node.type() == "Parent":
                code = str[0:1]
                str = str[1:]
                if code == "1":
                    node = node.childB
                elif code == "0":
                    node = node.childA
                else:
                    print("ERROR: RAN OUT OF DECODE")
                    return source_text
            # End stream for this letter, move on to next
            if(node.letter == "\b"):
                return source_text
            source_text = source_text + chr(node.ascii)
            success = self.increment_count_by_ascii(node.ascii)
            if success == False:
                print("ERROR: FAILED TO FIND ASCII")
                sys.exit()

        return source_text

huff = Huffman()

value = input("\n\nWelcome to the Adaptive Huffman Encoder\nEnter...\n1: Encode\n2: Decode\n")
while value != "1" and value != "2":
    value = input("\n\nEnter valid option.\n")
if value == "1":
    str = input("\n\nEnter your source text:\n")
    file = input("\n\nEnter desired filename to encode to:\n")
    bits = huff.adaptive_huffman_encode(str)
    with open(file, "wb") as f:
        if len(bits) % 16 != 0:
            bits += "0000000000000000"
        while len(bits) > 16:
            int_value = int(bits[:16], 2)
            bits = bits[16:]
            bin_array = struct.pack('i', int_value)
            f.write(bin_array)
if value == "2":
    file = input("\n\nEnter filename to decode from:\n")
    bits = "" #read file
    with open(file, "rb") as f:
        byte = f.read(4)
        arr = []
        while byte:
            bin_array = struct.unpack('i', byte)
            temp = str(bin(bin_array[0])[2:])
            while len(temp) < 16:
                temp = "0" + temp
            bits = bits + temp
            byte = f.read(4)
    str = huff.adaptive_huffman_decode(bits)
    print("Here is your decoded source text:\n" + str)
