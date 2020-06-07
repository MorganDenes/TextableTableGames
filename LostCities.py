from random import shuffle, randrange
import time


deck = []
hands = [[], []]
lastPlay = ["", ""]
newCard = ["", ""]
boards = {'R':[[], [], []],
          'Y':[[], [], []],
          'W':[[], [], []],
          'B':[[], [], []],
          'G':[[], [], []]}

curpl = 0
othpl = 1
discard = 2

def SwitchPlayer():
    global curpl, othpl
    othpl = curpl
    curpl = 1 - othpl

def GetCur():
    return curpl

def GetOth():
    return othpl


def PrintBoardSet(p, skip=False):
    mes = ""
    any = False
    for color, cards in boards.items():
        if len(cards[p]) != 0 or skip == False:
            any = True
            mes += "%s:%s\n"%(color, ''.join(cards[p]))
    return mes, any

def PrintHand():
    hands[curpl].sort()
    return " ".join((hands[curpl]))


def PrintGame():
    mes1, skip = PrintBoardSet(othpl)
    mes1 += '--\n'
    mes2, skip = PrintBoardSet(discard, skip=True)
    if skip:
        mes2 += '--\n'
    mes3, skip = PrintBoardSet(curpl)
    mes3 += "=%s==%i==%s=\n"%(lastPlay[othpl], len(deck), newCard[curpl])
    mes4 = PrintHand()
    return '-\n' + mes1 + mes2 + mes3 + mes4



def CreateDeck():
    global deck
    deck = []
    for color in boards:
        for face in ['$', '$'] + [x for x in faces]:
            deck.append(color + face)
    shuffle(deck)

def DrawHands():
    global hands
    hands = [[], []]
    for cards in range(8):
        for player in hands:
            player.append(DeckDraw())
            cards

def SetupGame():
    CreateDeck()
    DrawHands()



def DeckDraw():
    return deck.pop()



def BoardAddCard(p, card):
    boards[card[0]][p].append(card[1])

def BoardGetDiscard(pile):
    return pile + boards[pile][discard].pop()



def PromptPlayer():
    print(PrintGame())
    return input("Your move: ")



def GetCard(k):
    hands[curpl].remove(k)
    return k



def LegalMove(f):
    if len(boards[f[0]][curpl]) == 0:
        return True
    return faces[boards[f[0]][curpl][-1]] <= faces[f[1]]

colors = ['R','Y','W','B','G']
faces = {'$':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'X':10}
def ValidateMove(c):
    if len(c) < 1 or len(c) > 3:
        return False
    if (len(c[0]) == 2) and (c[0][0] in colors) and (c[0][1] in faces) and (c[0] in hands[curpl]):
        if len(c) > 1 and len(c[1]) == 1 and c[1] == 'M':
            if len(c) == 3 and len(c[2]) == 1 and c[2] in colors and len(boards[c[2]][discard]) > 0:
                if c[0][0] != c[2]:
                    return True
            elif len(c) == 2:
                return True
        elif len(c) == 2 and len(c[1]) == 1 and c[1] in colors and len(boards[c[1]][discard]) > 0:
            return LegalMove(c[0])
        elif len(c) == 1:
            return LegalMove(c[0])
    return False        

def HandleMove(m):
    commands = m.upper().split('.')
    if not ValidateMove(commands):
        return False
    
    index = 0
    card = GetCard(commands[index])
    lastPlay[curpl] = card
    index += 1

    if index < len(commands) and commands[index] == "M":
        BoardAddCard(discard, card)
        index += 1
    else:
        BoardAddCard(curpl, card)

    if index < len(commands):
        newCard[curpl] = BoardGetDiscard(commands[index])
    else:
        newCard[curpl] = DeckDraw()
    hands[curpl].append(newCard[curpl])
    return True



def CheckEndGame():
    return len(deck) == 0


def Score(p):
    totalScore = 0
    for color in boards:
        if len(boards[color][p]) == 0:
            continue
        colorScore = 0
        muliply = 1
        for card in boards[color][p]:
            if faces[card] == 1:
                muliply += 1
            else:
                colorScore += faces[card]
        totalScore += (colorScore - 20) * muliply + (20 if len(boards[color][p]) >= 8 else 0)
    return totalScore


def Play():
    SetupGame()
    while True:
        move = PromptPlayer()
        if HandleMove(move):
            SwitchPlayer()
            if CheckEndGame():
                break
        else:
            print("Invalid move.")
    score1 = Score(0)
    score2 = Score(1)
    print(score1)
    print(score2)



# Play()
