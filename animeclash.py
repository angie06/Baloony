#OPIANA|BERMILLO|MADRASO(GAMEDEV BSIT3C)
import random, pygame, sys
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 700 # size of window's width in pixels
WINDOWHEIGHT = 550 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 100 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 5 # number of columns of icons
BOARDHEIGHT = 4 # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

background = pygame.image.load("k.gif")
backgroundRect = background.get_rect()
size = (WINDOWWIDTH , WINDOWHEIGHT)
screen = pygame.display.set_mode(size)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

ANIME1='anime1'
ANIME2='anime2'
ANIME3='anime3'
ANIME4='anime4'
ANIME5='anime5'
ANIME6='anime6'
ANIME7='anime7'
ANIME8='anime8'
ANIME9='anime9'
ANIME10='anime10'
#ANIME11='anime11'
#ANIME12='anime12'
#ANIME13='anime13'
#ANIME14='anime14'
#ANIME15='anime15'
#ANIME16='anime16'
#ANIME17='anime17'
#ANIME18='anime18'
#ANIME19='anime19'
#ANIME20='anime20'
#ANIME21='anime21'
#ANIME22='anime22'
#ANIME23='anime23'
#ANIME24='anime24'
#ANIME25='anime25'
#ANIME26='anime26'
#ANIME27='anime27'
#ANIME28='anime28'
#ANIME29='anime29'
#ANIME30='anime30'
#ANIME31='anime31'
#ANIME32='anime32'
#ANIME33='anime33'
#ANIME34='anime34'
#ANIME35='anime35'

ALLCOLORS = (RED)
ALLANIME = (ANIME1, ANIME2, ANIME3, ANIME4, ANIME5, ANIME6, ANIME7, ANIME8, ANIME9, ANIME10)#, ANIME11, ANIME12, ANIME13, ANIME14, ANIME15, ANIME16, ANIME17, ANIME18, ANIME19, ANIME20)# ANIME21, ANIME22, ANIME23, ANIME24, ANIME25, ANIME26, ANIME27, ANIME28, ANIME29, ANIME30, ANIME31, ANIME32, ANIME33, ANIME34, ANIME35)
assert len(ALLCOLORS) * len(ALLANIME) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('ANIME CLASH')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of the first box clicked.

    screen.blit(background, backgroundRect)
    startGameAnimation(mainBoard)

    while True: # main game loop
        mouseClicked = False

        screen.blit(background, backgroundRect) # drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else: # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1anime, icon1color = getAnime(mainBoard, firstSelection[0], firstSelection[1])
                    icon2anime, icon2color = getAnime(mainBoard, boxx, boxy)

                    if icon1anime != icon2anime :
                        pygame.mixer.music.load('foghorn.wav')
                        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
                        pygame.mixer.music.play()
                        # Icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes): # check if all pairs found
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        # Reset the board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # Show the fully unrevealed board for a second.
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation.
                        startGameAnimation(mainBoard)
                    firstSelection = None # reset firstSelection variable

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for anime in ALLANIME:
            icons.append( (anime, color) )

    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2 # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(anime, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half =    int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Get anime images
    if anime == ANIME1:
        img=pygame.image.load("ani1.gif")
        DISPLAYSURF.blit(img,(left,top))
    elif anime == ANIME2:
        img=pygame.image.load("ani2.gif")
        DISPLAYSURF.blit(img,(left,top))
    elif anime == ANIME3:
        img=pygame.image.load("ani3.gif")
        DISPLAYSURF.blit(img,(left,top))
    elif anime == ANIME4:
        img=pygame.image.load("ani4.gif")
        DISPLAYSURF.blit(img,(left,top))
    elif anime == ANIME5:
        img=pygame.image.load("ani5.gif")
        DISPLAYSURF.blit(img,(left,top))
    elif anime == ANIME6:
        img=pygame.image.load("ani6.gif")
        DISPLAYSURF.blit(img,(left,top))
    elif anime == ANIME7:
        img=pygame.image.load("ani7.gif")
        DISPLAYSURF.blit(img,(left,top))
    elif anime == ANIME8:
        img=pygame.image.load("ani8.gif")
        DISPLAYSURF.blit(img,(left,top))
    elif anime == ANIME9:
        img=pygame.image.load("ani9.gif")
        DISPLAYSURF.blit(img,(left,top))
    elif anime == ANIME10:
        img=pygame.image.load("koroko.gif")
        DISPLAYSURF.blit(img,(left,top))
    #elif anime == ANIME11:
     #   img=pygame.image.load("lo.gif")
      #  DISPLAYSURF.blit(img,(left,top))
    #elif anime == ANIME12:
     #   img=pygame.image.load("ld.gif")
      #  DISPLAYSURF.blit(img,(left,top))
    #elif anime == ANIME13:
     #   img=pygame.image.load("question.gif")
      #  DISPLAYSURF.blit(img,(left,top))
    #elif anime == ANIME14:
     #   img=pygame.image.load("lk.gif")
      #  DISPLAYSURF.blit(img,(left,top))
    #elif anime == ANIME15:
     #   img=pygame.image.load("lo.gif")
      #  DISPLAYSURF.blit(img,(left,top))
    #elif anime == ANIME16:
     #   img=pygame.image.load("ld.gif")
      #  DISPLAYSURF.blit(img,(left,top))
    #elif anime == ANIME17:
     #   img=pygame.image.load("question.gif")
      #  DISPLAYSURF.blit(img,(left,top))
    #elif anime == ANIME18:
     #   img=pygame.image.load("lk.gif")
      #  DISPLAYSURF.blit(img,(left,top))
    #elif anime == ANIME19:
     #   img=pygame.image.load("lo.gif")
      #  DISPLAYSURF.blit(img,(left,top))
    #elif anime == ANIME20:
     #   img=pygame.image.load("ld.gif")
      #  DISPLAYSURF.blit(img,(left,top))
   # elif anime == ANIME21:
   #     img=pygame.image.load("question.gif")
   #     DISPLAYSURF.blit(img,(left,top))
   # elif anime == ANIME22:
    #    img=pygame.image.load("lk.gif")
    #    DISPLAYSURF.blit(img,(left,top))
   # elif anime == ANIME23:
   #     img=pygame.image.load("lo.gif")
   #     DISPLAYSURF.blit(img,(left,top))
   # elif anime == ANIME24:
   #     img=pygame.image.load("ld.gif")
   #     DISPLAYSURF.blit(img,(left,top))
   # elif anime == ANIME25:
   #     img=pygame.image.load("question.gif")
   #     DISPLAYSURF.blit(img,(left,top))
   # elif anime == ANIME26:
    #    img=pygame.image.load("lk.gif")
    #    DISPLAYSURF.blit(img,(left,top))
   # elif anime == ANIME27:
   #     img=pygame.image.load("lo.gif")
   #     DISPLAYSURF.blit(img,(left,top))
  #  elif anime == ANIME28:
   #     img=pygame.image.load("ld.gif")
   #     DISPLAYSURF.blit(img,(left,top))
   # elif anime == ANIME29:
   #     img=pygame.image.load("question.gif")
   #     DISPLAYSURF.blit(img,(left,top))
   # elif anime == ANIME30:
   #     img=pygame.image.load("lk.gif")
   #     DISPLAYSURF.blit(img,(left,top))
  #  elif anime == ANIME31:
    #    img=pygame.image.load("lo.gif")
   #     DISPLAYSURF.blit(img,(left,top))
   # elif anime == ANIME32:
   #     img=pygame.image.load("ld.gif")
   #     DISPLAYSURF.blit(img,(left,top))
   # elif anime == ANIME33:
   #     img=pygame.image.load("question.gif")
   #     DISPLAYSURF.blit(img,(left,top))
   # elif anime == ANIME34:
   #     img=pygame.image.load("lk.gif")
    #    DISPLAYSURF.blit(img,(left,top))
   # elif anime == ANIME35:
    #    img=pygame.image.load("lo.gif")
    #    DISPLAYSURF.blit(img,(left,top))


def getAnime(board, boxx, boxy):
    # anime value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        anime, color = getAnime(board, box[0], box[1])
        drawIcon(anime, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon.
                anime, color = getAnime(board, boxx, boxy)
                drawIcon(anime, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color2 = pygame.image.load("k.gif")
    color1 = pygame.image.load("p.gif")

    for i in range(13):
        pygame.mixer.music.load('yipee.wav')
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        pygame.mixer.music.play()

        color1, color2 = color2, color1 # swap colors
        DISPLAYSURF.blit(color1,(0,0))
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True


if __name__ == '__main__':
    main()
    
