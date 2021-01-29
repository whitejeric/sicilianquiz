import re

class PcMover:

    def __init__(self):
        self.maxMoves = 0
        self.moveList = {}

    def insertMoveN(self, moves):
        if moves:
            self.maxMoves +=1
            self.moveList[self.maxMoves] = moves

    def populateMoves(self, line):
        if line:
            line.split('')
            # /[W].*?[V|X]


    def __str__(self):
        arr = []
        string = ""

        for num,moves in self.moveList.items():
            print("Possible moves at turn " + str(num))
            print(moves)

        return string

mover = PcMover()
mover.insertMoveN(['e4', 'c5'])
# print(mover)
# with open("dict.txt", 'r') as sicdefs:
#     for line in sicdefs:
#         sic = line.split('X')
#         moves, name = sic[0], sic[1].strip()
#         linedict[name] = moves
#         print(name, moves)

print(re.findall('[W](.*?)[V|X]', 'We4Vc5Wnf3Vnc6Wd4X'))

# words = open(DICTIONARY, "rt").read().split()
#
# linedict = {}
#
# with open("dict.txt", 'r') as sicdefs:
#     for line in sicdefs:
#         sic = line.split('X')
#         moves, name = sic[0], sic[1].strip()
#         linedict[name] = moves
#         print(name, moves)
#
# linedict = sorted(linedict.items(), key=operator.itemgetter(1)) #sort by moves, not line name
# print(m.group(1))
# We4Vc5Wnf3Vnc6Wd4X(Open_Nc6)
