import re
from niceLine import toRow#, toCols
from random import seed, randint, shuffle

class whiteMoves:

    def __init__(self):
        self.moveList = []

    def __len__(self):
        return len(self.moveList)

    def insertLine(self, line): #line is an array of just the white moves of a line
        if line:
            line = re.findall('[W](.*?)[V|X]', line)
            # print (line)
            for i, move in enumerate(line):
                # print(line[i])
                if i >= len(self.moveList):
                    self.moveList.append([])
                    # print(self.moveList)
                if move not in self.moveList[i]:
                    self.moveList[i].append(move)
                    # print(self.moveList[i])
                # print(i, self.moveList[i])

    def getMovesAt(self, i):
        return self.moveList[i]

    def randomMove(self, turn):
        possible = self.getMovesAt(turn)
        value = randint(0, len(possible)-1)
        shuffle(possible)
        return 'W' + possible[value]

    def __str__(self):
        string =''
        for num, moves in enumerate(self.moveList):
            string += "Possible white moves at turn {0} are {1} \n".format(str(num+1), moves)
        return string

# # mover = whiteMoves()
# # mover.insertLine(['e4', 'c5'])
# # mover.insertLine(re.findall('[W](.*?)[V|X]', 'We4Vc5Wnf3Vnc6Wd4X'))
# print(toRow('We4Vc5Wnf3Vnc6Wd4X'))
# mover.insertLine('We4Vc5Wnf3Vnc6Wd4X')
#
# print(toRow('We4Vc5Wnf3Vd6Wd4Vcxd4Wnxd4Vnf6Wnc3Va6X'))
# mover.insertLine('We4Vc5Wnf3Vd6Wd4Vcxd4Wnxd4Vnf6Wnc3Va6X')
#
# print(toRow('We4Vc5Wnf3Vd6Wd4Vcxd4Wnxd4Vnf6Wnc3Vnc6X'))
# mover.insertLine('We4Vc5Wnf3Vd6Wd4Vcxd4Wnxd4Vnf6Wnc3Vnc6X')
#
# print(toRow('We4Vc5Wnf3Vd6Wd4X'))
# mover.insertLine('We4Vc5Wnf3Vd6Wd4X')
#
# print(toRow('We4Vc5Wnf3Ve6Wd4X'))
# mover.insertLine('We4Vc5Wnf3Ve6Wd4X')
#
# print(toRow('We4Vc5WNf3VNc6WNf3X'))
# mover.insertLine('We4Vc5WNf3VNc6WNf3X')
#
# mover.insertLine('We4Vc5WNf7VNc6WNf3X')
# mover.insertLine('We4Vc5WNf6VNc6WNf3X')
# mover.insertLine('We4Vc5WNf5VNc6WNf3X')
# mover.insertLine('We4Vc5WNf4VNc6WNf3X')
#
# print(mover.getMovesAt(1))
# print(mover.randomMove(1))
#
# print(mover.moveList)
# print(mover)
# # what we want: whiteMoves.nextMove(turn number, line so far)
# # print(mover)
# # with open("dict.txt", 'r') as sicdefs:
# #     for line in sicdefs:
# #         sic = line.split('X')
# #         moves, name = sic[0], sic[1].strip()
# #         linedict[name] = moves
# #         print(name, moves)
#
# # print(re.findall('[W](.*?)[V|X]', 'We4Vc5Wnf3Vnc6Wd4X'))
#
# # words = open(DICTIONARY, "rt").read().split()
# #
# # linedict = {}
# #
# # with open("dict.txt", 'r') as sicdefs:
# #     for line in sicdefs:
# #         sic = line.split('X')
# #         moves, name = sic[0], sic[1].strip()
# #         linedict[name] = moves
# #         print(name, moves)
# #
# # linedict = sorted(linedict.items(), key=operator.itemgetter(1)) #sort by moves, not line name
# # print(m.group(1))
# # We4Vc5Wnf3Vnc6Wd4X(Open_Nc6)
