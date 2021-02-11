import re
#spruce up the printing of each line
#input form of: We4Vc5Wnf3Vd6Wd4Vcxd4Wnxd4Vnf6Wnc3X(Open_Classical) or without name

def row(l,c,r):
    return '{0:<3}{1:<5}{2:<5}\n'.format(l, c, r)

def toCols(WVXLine, name=''):
    moveCount = 0
    inCols = ''
    wMoves = re.findall('[W](.*?)[V|X]', WVXLine)
    bMoves = re.findall('[V](.*?)[W|X]', WVXLine)
    if name: inCols += name + '\n'
    i = 0
    while i < len(bMoves):
        inCols += (row(str(i+1) +'.', wMoves[i], bMoves[i]))
        i+=1
    if len(bMoves) < len(wMoves): #possible hanging white line:
        inCols += (row(str(i+1)+'.', wMoves[i], ''))
    return inCols

def toRow(WVXLine, name=''):
    moveCount = 0
    wMoves = re.findall('[W](.*?)[V|X]', WVXLine)
    bMoves = re.findall('[V](.*?)[W|X]', WVXLine)
    i = 0
    niceRow = ''
    if name: niceRow += name +': '
    while i < len(bMoves):
        niceRow += ('{0}.{1} {2} '.format(str(i+1), wMoves[i], bMoves[i]))
        i+=1
    if len(bMoves) < len(wMoves): #possible hanging white line:
        niceRow += ('{0}.{1} {2} '.format(str(i+1), wMoves[i], ''))
    return niceRow

if 0:
    return
# print(toCols('We4Vc5Wnf3Vd6Wd4Vcxd4Wnxd4Vnf6Wnc3X', '(Open_Classical)'))
# print(toRow('We4Vc5Wnf3Vd6Wd4Vcxd4Wnxd4Vnf6Wnc3X(Open_Classical)'))
