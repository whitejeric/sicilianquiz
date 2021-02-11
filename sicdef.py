#!/usr/bin/python3
# By Steve Hanov, 2011. Released to the public domain.
# Please see http://stevehanov.ca/blog/index.php?id=115 for the accompanying article.
#
# Based on Daciuk, Jan, et al. "Incremental construction of minimal acyclic finite-state automata."
# Computational linguistics 26.1 (2000): 3-16.
#
# Updated 2014 to use DAWG as a mapping; see
# Kowaltowski, T.; CL. Lucchesi (1993), "Applications of finite automata representing large vocabularies",
# Software-Practice and Experience 1993
import sys
import operator
import time
from whiteMoves import whiteMoves
from niceLine import toRow, toCols

# DICTIONARY = "dict.txt"
# QUERY = sys.argv[1:] +'We4Vc5Wnf3Vnc6Wd4X We4Vc5Wnf3Ve6Wd4X We4Vc5Wnf3Vd6Wd4X We4Vc5Wnf3Vd6Wd4Vcxd4Wnxd4Vnf6Wnc3VNc6X We4Vc5Wnf3Vd6Wd4Vcxd4Wnxd4Vnf6Wnc3Va6X'


# This class represents a node in the directed acyclic word graph (DAWG). It
# has a list of edges to other nodes. It has functions for testing whether it
# is equivalent to another node. Nodes are equivalent if they have identical
# edges, and each identical edge leads to identical states. The __hash__ and
# __eq__ functions allow it to be used as a key in a python dictionary.
class DawgNode:
    NextId = 0

    def __init__(self):
        self.id = DawgNode.NextId
        DawgNode.NextId += 1
        self.final = False #end node for a complete line
        self.bMove = False #end node substring terminating after a black move
        self.wMove = False #end node substring terminating after a white move
        self.edges = {}

        # Number of end nodes reachable from this one.
        self.count = 0

    def __str__(self):
        arr = []
        if self.final:
            arr.append("1")
        else:
            arr.append("0")

        for (label, node) in self.edges.items():
            arr.append( label )
            arr.append( str( node.id ) )

        return "_".join(arr)

    def __hash__(self):
        return self.__str__().__hash__()

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def numReachable(self):
        # if a count is already assigned, return it
        if self.count: return self.count

        # count the number of final nodes that are reachable from this one.
        # including self
        count = 0
        if self.final: count += 1
        for label, node in self.edges.items():
            count += node.numReachable()

        self.count = count
        return count

class Dawg:
    def __init__(self):
        self.previousWord = ""
        self.root = DawgNode()

        # Here is a list of nodes that have not been checked for duplication.
        self.uncheckedNodes = []

        # Here is a list of unique nodes that have been checked for
        # duplication.
        self.minimizedNodes = {}

        # Here is the data associated with all the nodes
        self.data = []

    def insert( self, word, data ):
        if word <= self.previousWord:
            raise Exception("Error: Words must be inserted in alphabetical " +
                "order.")
        # print("Inserting: " + word +"Previous: "+ self.previousWord)
        # find common prefix between word and previous word
        commonPrefix = 0
        for i in range( min( len( word ), len( self.previousWord ) ) ):
            if word[i] != self.previousWord[i]: break
            commonPrefix += 1

        # Check the uncheckedNodes for redundant nodes, proceeding from last
        # one down to the common prefix size. Then truncate the list at that
        # point.
        self._minimize( commonPrefix )

        self.data.append(data)

        # add the suffix, starting from the correct node mid-way through the
        # graph
        if len(self.uncheckedNodes) == 0:
            node = self.root
        else:
            node = self.uncheckedNodes[-1][2]

        for letter in word[commonPrefix:]:
            nextNode = DawgNode()
            node.edges[letter] = nextNode
            self.uncheckedNodes.append( (node, letter, nextNode) )
            if letter == 'W':
                node.bMove = True #node has an edge to a white move in the set
            if letter == 'V':
                node.wMove = True #node has an edge to a black move in the set
            node = nextNode
        node.final = True
        self.previousWord = word

    def finish( self ):
        # minimize all uncheckedNodes
        self._minimize( 0 );

        # go through entire structure and assign the counts to each node.
        self.root.numReachable()

    def _minimize( self, downTo ):
        # proceed from the leaf up to a certain point
        for i in range( len(self.uncheckedNodes) - 1, downTo - 1, -1 ):
            (parent, letter, child) = self.uncheckedNodes[i];
            if child in self.minimizedNodes:
                # replace the child with the previously encountered one
                parent.edges[letter] = self.minimizedNodes[child]
            else:
                # add the state to the minimized nodes.
                self.minimizedNodes[child] = child;
            self.uncheckedNodes.pop()

    def lookup( self, word ):
        node = self.root
        skipped = 0 # keep track of number of final nodes that we skipped
        for letter in word:
            if letter not in node.edges:
                return None
            for label, child in sorted(node.edges.items()):
                if label == letter:
                    if node.final:
                        skipped += 1
                    node = child
                    break
                skipped += child.count
        available = node.numReachable()
        if node.final:
            return self.data[skipped]
        if node.bMove:
            return "a substring ending in a black move with {0} line(s) containing it in the set".format(available)
            #make a system for complete lines that are also sublines
            #ie basic open is only 4 moves long, give it 50% chance of just ending?
        if node.wMove:
            return "a substring ending in a white move with {0} line(s) containing it in the set".format(available)


    def nodeCount( self ):
        return len(self.minimizedNodes)

    def edgeCount( self ):
        count = 0
        for node in self.minimizedNodes:
            count += len(node.edges)
        return count

    def display(self):
        stack = [self.root]
        done = set()
        while stack:
            node = stack.pop()
            if node.id in done: continue
            done.add(node.id)
            print("{}: ({})".format(node.id, node))
            for label, child in node.edges.items():
                print("    {} goto {}".format(label, child.id))
                stack.append(child)

    def whiteMove(self, line):
        return 0


if 0:
    dawg = Dawg()
    dawg.insert("cat", 0)
    dawg.insert("catnip", 1)
    dawg.insert("zcatnip", 2)
    dawg.finish()
    dawg.display()
    sys.exit()

dawg = Dawg()
compMoves = whiteMoves()
DICTIONARY = "dictchess.txt"
WordCount = 0
# words = open(DICTIONARY, "rt").read().split()

linedict = {}
QUERY = {}
name = 0
with open(DICTIONARY, 'rt') as sicdefs:
    for line in sicdefs:
        sic = line.split('X')
        moves, name = sic[0] + 'X', sic[1].strip()
        linedict[name] = moves
        compMoves.insertLine(moves)

linedict = sorted(linedict.items(), key=operator.itemgetter(1)) #sort by moves, not line name
QUERY = linedict
print(linedict)


start = time.time()
for name, moves in linedict:
    WordCount += 1
    dawg.insert(moves, name)
    if ( WordCount % 100 ) == 0: print("{0}\r".format(WordCount), end="")
dawg.finish()
print("Dawg creation took {0} s".format(time.time()-start))

EdgeCount = dawg.edgeCount()
print("Read {0} words into {1} nodes and {2} edges".format(
    WordCount, dawg.nodeCount(), EdgeCount))

print("This could be stored in as little as {0} bytes".format(EdgeCount * 4))


QUERY.append(('(test)','We4Vc5WNf3')) #semi complete test case

#ensure all lines have been properly inserted into the dawg
for name, word in QUERY:
    result = dawg.lookup(word)
    print("Q:  {0} aka the {1}".format(word, name))
    if result == None:
        print("A: {0} not in dictionary.\n".format(toRow(word)))
    # elif result == name: #making super sure
    else:
        if word[:-1] != 'X': #to test semi complete lines as queries
            word += 'X'
        cResult = result.replace('(', '').replace(')', '')
        print("A: {0} is in the dictionary as the {1}\n".format(toRow(word), result))

# print dawg.lookup('We4Vc5Wnf3')
# dawg.display()
read = 'W'
temp = ''
black = False #true when it is blacks turn
quit = False
print(compMoves)
while quit != True:
    temp = input('Enter a move: ')
    if temp == 'q':
        break
    result = dawg.lookup(read+temp)
    if result == None:
        print("A: {0} not in dictionary.".format(read+temp))
        temp = ''
    else:
        print("A: {0} is in the dictionary as the {1}".format(read+temp, result))
        result = None
        if black == False:
            read += temp + 'V'
            black = True #now its blacks turn
        else:
            read += temp + 'W'
            black = False #whites turn
        # while black == False:
        #     temp = input('Enter a black move: ')
        #     result = dawg.lookup(read+temp)
        #     if result == None:
        #         print("A: {0} not in dictionary.".format(read+temp))
        #         temp = ''
        #     else:
        #         print("A: {0} is in the dictionary as the {1}".format(read+temp, result))
        #         read += temp + 'W'
        #         black = True
