from typing import List, Tuple, Set
from copy import deepcopy
class TrieNode:
    def __init__(self, letter=None,end_of_word = False) -> None:
        self.letter = letter
        self.stem_set = set()
        # add attributes for whether it is the end of a word and a collection of pointers to
        # next letters

        self.is_end_of_word = end_of_word
#       self.pointer = {'a':None,'b':None,'c':None,'d':None,'e':None,'f':None,'g':None,'h':None,'i':None,'j':None,'k':None,'l':None,'m':None,'n':None,'o':None,'p':None,'q':None,'r':None,'s':None,'t':None,'u':None,'v':None,'w':None,'x':None,'y':None,'z':None,}
        self.pointer = {}

class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()
        self.words = ""
    def generate_tree_from_file(self)->None:
        words = self._load_words()
        #add code here to set up the TrieNode tree structure for the words
        for word in words:
            # if (word == "quest"):
            #      print("hi")
            current_node = self.root
            for index in range(len(word)-1,-1,-1):
                next_letter = str(word[index])

                if next_letter in current_node.pointer and index !=0:
                    current_node = current_node.pointer[next_letter]

                else:

                    #we need to make the first letter is_end_of_word= True
                    if index ==0:
                        #this if is for when we only need to replace  is_end_of_word to be true which the else statement won't do (it would either keep is_end_of_word to be false or delete pointer values)
                        if next_letter in current_node.pointer: 
                            current_node.pointer[next_letter].is_end_of_word =True
                        else:
                            
                            current_node.pointer[next_letter] = TrieNode(next_letter,True)
                        break
                    else:
                        current_node.pointer[next_letter] = TrieNode(next_letter)
                    current_node = current_node.pointer[next_letter]
                    #print(current_node)
            #current_node.is_end_of_word = True
    
    def search(self, input)->bool:
        curr = self.root
        for i in input:
            if (curr.pointer[i] == None):
                return (False, False)
            curr = curr.pointer[i]
        return (True, curr)

        

    # helper to load words. No modifications needed
    def _load_words(self):
        words = []
        with open("words.txt", "r", encoding="utf-8") as file:
            for line in file:
                word = line.strip()
                words.append(word)
        return words

# Implement the Boggled Solver. This Boggle has the following special properties:
# 1) All words returned should end in a specified suffix (i.e. encode the trie in reverse)
# 2) Board tiles may have more than 1 letter (e.g. "qu" or "an")
# 3) The number of times you can use the same tile in a word is variable
# Your implementation should account for all these properties.
class Boggled:
    def  __init__(self):
        self.trie = Trie()
        self.trie.generate_tree_from_file()
        self.boggle_board = []
        self.max_uses_board = []
        self.suffix = ""
        self.set_of_words = set()
    # setup test initializes the game with the game board and the max number of times we can use each 
    # tile per word
    def setup_board(self, max_uses_per_tile: int, board:List[List[str]])->None:
        self.boggle_board = board

        # for y in board:
        #     for x in board:
        #         self.boggle_board[y][x] = (board[y][x], max_uses_per_tile)
        self.max_uses_board = [[0] * len(board) for _ in range(len(board))]
        for y in range(len(board)):
            for x in range(len(board)):
                self.max_uses_board[y][x] = max_uses_per_tile
    # Returns a set of all words on the Boggle board that end in the suffix parameter string. Words can be found
    # in all 8 directions from a position on the board
    def get_all_words(self, suffix:str)->Set:
        current_letter = self.boggle_board[0][0]
        current_node = self.trie.root.pointer[current_letter]
        self.suffix = suffix
        
    
        for y in range(len(self.boggle_board)):
            for x in range(len(self.boggle_board)):
                #we start with letters that are the last letter of suffix
                # case after "or" doesn't work
                if self.boggle_board[y][x] in self.trie.root.pointer and self.boggle_board[y][x] == suffix[-1] or self.boggle_board[y][x] in self.trie.root.pointer and self.boggle_board[y][x] == suffix[::-1][0:2]:
                    # if len(self.trie.root.pointer[self.boggle_board[y][x]].letter) >1:
                    #     self.get_all_words_recursive(x,y,"",self.trie.root.pointer[self.boggle_board[y][x]],self.max_uses_board)
                    # else:
                    self.get_all_words_recursive(x,y,"",self.trie.root.pointer[self.boggle_board[y][x]],self.max_uses_board)
        return_set = set()
        for i in self.set_of_words:
            if len(i) > len(suffix):
                return_set.add(i)
        #we do the above becuase of last line of generate_tree_from_file
        print (return_set)
        return(return_set)

    # recursive helper for get_all_words. Customize parameters as needed; you will likely need params for 
    # at least a board position and tile
    #important!: we look for words backwards so we find tar instead of rat 
    def get_all_words_recursive(self,x,y,word,current_node,uses_board):

        # CHOOSE (try placing )
        # EXPLORE ( recursei to place the rest in next spot)
        
        if uses_board[y][x] == 0:
          
            return()
        
        uses_board[y][x] -=1
        # if len(current_node.letter) >1:
        #     word += "uq"
        # else:
        word+=current_node.letter
        #this if checks if last letters are suffix
        if current_node.is_end_of_word == True and self.suffix[::-1] in word[:len(self.suffix)]:
            #we add the word reversed so it's normal
            self.set_of_words.add(word[::-1])
        
        #important!: we look for words backwards so we find tar instead of rat 

        next_directions = self.get_8_directions(x,y)
        for direction in next_directions:
            #case...
            if len(word) < len(self.suffix) and current_node.letter not in self.suffix: 
                return()
            #recursive!!!
            if len(self.boggle_board[direction[1]][direction[0]]) >1 and self.boggle_board[direction[1]][direction[0]][1] in current_node.pointer and self.boggle_board[direction[1]][direction[0]][0] in current_node.pointer[self.boggle_board[direction[1]][direction[0]][1]].pointer:
                current_node = current_node.pointer[self.boggle_board[direction[1]][direction[0]][1]]
                #if self.boggle_board[direction[1]][direction[0]][0] in current_node.pointer:

                #we use .search because it searches the trie not going current_node by current_node
                z = self.trie.search(word + self.boggle_board[direction[1]][direction[0]][::-1])
                if (z[0]):
                    ##true case, can continue on recursing
                    own_uses_board = deepcopy(uses_board)
                    self.get_all_words_recursive(direction[0],direction[1],word + self.boggle_board[direction[1]][direction[0]][1],z[1],own_uses_board)
                else:
                    ##false case, we just return
                    return()
            else:        
                if self.boggle_board[direction[1]][direction[0]] in current_node.pointer:
                    #word += current_node.letter
                    own_uses_board = deepcopy(uses_board)
                    self.get_all_words_recursive(direction[0],direction[1],word,current_node.pointer[self.boggle_board[direction[1]][direction[0]]],own_uses_board)
        # UNCHOOSE (remove the letter so we try another spot)
        
        uses_board[y][x] +=1      
        
    def get_8_directions (self,x,y) -> List[Tuple]:
        directions = [
        [0, -1],    # up
        [1, -1],    # up right
        [1, 0],     # right
        [1, 1],     # down right
        [0, 1],     # down
        [-1, 1],    # down left
        [-1, 0],    # left
        [-1, -1],   # left up
        ]
        list_of_cords=[]
        for i in directions:    
            if x+i[0] in range(len(self.boggle_board)) and y+i[1] in range(len(self.boggle_board)):

                #next_pos = boggle_board[y+i[1]][x+i[0]]
                list_of_cords.append((x+i[0],y+i[1]))
        return list_of_cords
