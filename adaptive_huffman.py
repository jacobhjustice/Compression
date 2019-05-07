import string

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

class Node:
    def __init__(self, letterA, letterB):
        self.letterA = letterA
        self.letterB = letterB

    def get_count(self):
        return self.letterA.get_count() + self.letterB.get_count()

    def get_ascii(self):
        asciiA = self.letterA.get_ascii()
        asciiB = self.letterB.get_ascii()
        return asciiA if asciiA > asciiB else asciiB

class Huffman_Tree:
    valid_characters = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    def init(self):
        arr = []
        for i in range(len(self.valid_characters)):
            char = self.valid_characters[i]
            arr.append(Letter(char, 32 + i, 1))
        return arr
    def build(self):
        arr = self.init()
        arr.reverse()
        
        while len(arr) > 1:
            # Smallest letter
            minA = Letter(None, 999, 999)
            # Second smallest letter
            minB = Letter(None, 999, 999)

            for letter in arr:
                if letter.get_count() < minA.get_count():
                    minB = minA
                    minA = letter
                elif letter.get_count() < minB.get_count():
                    minB = letter
            node = Node(minA, minB)
            arr.remove(minA)
            index = arr.index(minB)
            arr[index] = node
            for i in arr:
                print(i.get_count())
            print("________________________")
        

# def adaptive_huffman_encode(str):
#     for chr in str:
#         print(chr)


# adaptive_huffman_encode("test")

tree = Huffman_Tree()
tree.build()