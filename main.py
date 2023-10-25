"""
Welcome to my chess program!

Here is a link to the spritework that I used... https://opengameart.org/content/chess-pieces-and-board-squares
"""

import pygame
import time

#GLOBAL CONSTANTS
running = True
WIDTH = 500
HEIGHT = 600
WHITE = pygame.Color("#f8f3f1")
BLACK = pygame.Color("#4e3023")
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
xaxisList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] #From left to right
yaxisList = [8, 7, 6, 5, 4, 3, 2, 1] #From top to bottom

#Class for all board squares, used for mouse tracking and display
class Square:
    def __init__(self, color, locationx, locationy, xaxis, yaxis):
        self.locationx = locationx
        self.locationy = locationy
        self.color = color
        self.beginColor = color
        self.xaxis = xaxis #Xaxis and Yaxis values are for deciding if moves are legal later on
        self.yaxis = yaxis
        #occupied and piece are for tracking who is in said space.
        self.occupied = False
        self.piece = None #Contains a pointer to the object that is in this square
        self.selected = False
        self.possibleLocation = False

    def getPos(self):
        return self.locationx, self.locationy
    
    def getColor(self):
        return self.color
    
    def hover(self):
        #Set hover color
        self.color = pygame.Color("#00e2e2")

    def resetColor(self): 
        #Reset color to initial color when not hovering
        if self.selected == True:
            self.color = pygame.Color("#00e2e2")
        else:
            self.color = self.beginColor

    def setPiece(self, piece):
        self.piece = piece
        self.occupied = True

    def getPiece(self):
        return self.piece

    def getAxis(self):
        return self.xaxis,self.yaxis

    def getOccupied(self):
        return self.occupied
    
    def select(self):
        self.selected = True
    def unselect(self):
        self.selected = False
    def getSelected(self): #Get whether the square is selected
        return self.selected
    def setPossible(self):
        self.possible = True
    def resetPossible(self):
        self.possible = False
    def removePiece(self):
        self.occupied = False
        self.piece = None

class Piece:
    def __init__(self, square, type, team, image):
        self.square = square
        self.type = type
        self.team = team
        self.image = pygame.image.load(image)
        self.firstMove = True
        self.alive = True

    def setSquare(self, newSquare): #Move to new square
        self.square = newSquare


    def getTeam(self):
        return self.team
    
    def getType(self):
        return self.type

    def die(self): #Unlink the piece from the square
        self.square = None
        self.alive = False

    def getAlive(self):
        return self.alive

    def getImage(self):
        return self.image

    def getSquare(self):
        return self.square
    
    def pawnMoved(self):
        self.firstMove = False
    #For pawns, gets if the pawn hasn't moved yet
    def getFirst(self):
        return self.firstMove


#Init all of the square objects for the board
def initSquares():
    squares = []
    
    row = 0
    column = 0
    posx = 50
    posy = 100
    for i in range(64): 
            if row % 2 == 0:
                if i % 2 == 0:
                    color = WHITE
                else: 
                    color = BLACK
            else:
                if i % 2 == 0:
                    color = BLACK
                else: 
                    color = WHITE
            
            square = Square(color, posx, posy, xaxisList[column], yaxisList[row]) #Create Square
            squares.append(square)

            if posx == 400:
                posy += 50
                posx = 50
                row += 1
                column = 0
            else:
                posx += 50
                column += 1
    return squares
#Gets axis indexes for square, returns x, y indexes
def getAxis(xaxis, yaxis):
    for index, axis in enumerate(xaxisList):
        if axis == xaxis:
            xindex = index
    for index, axis in enumerate(yaxisList):
        if axis == yaxis:
            yindex = index
    return xindex, yindex

#Init all pieces for the board and assign them to squares
def initPieces(squares):
    types = [0,1,2,3,4,2,1,0,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,0,1,2,3,4,2,1,0,] 
    pieces = []
    squareIndex = 0

    #Set all attributes for starting pieces
    for i in range(32):
        if i < 16:
            team = 0 #Team 0 is Black
        else:
            team = 1 #Team 1 is White
            squareIndex = i + 32

        if types[i] == 0: #Rooks
            if team == 0:
                sprite = "sprites\\b_rook_png_128px.png"
            else:
                sprite = "sprites\\w_rook_png_128px.png"        
        elif types[i] == 1: #Knights
            if team == 0:
                sprite = "sprites\\b_knight_png_128px.png"
            else:
                sprite = "sprites\\w_knight_png_128px.png"
        elif types[i] == 2: #Bishops
            if team == 0:
                sprite = "sprites\\b_bishop_png_128px.png"
            else:
                sprite = "sprites\\w_bishop_png_128px.png"
        elif types[i] == 3: #Queens
            if team == 0:
                sprite = "sprites\\b_queen_png_128px.png"
            else:
                sprite = "sprites\\w_queen_png_128px.png"
        elif types[i] == 4: #King
            if team == 0:
                sprite = "sprites\\b_king_png_128px.png"
            else:
                sprite = "sprites\\w_king_png_128px.png"
        elif types[i] == 5: #Pawns
            if team == 0:
                sprite = "sprites\\b_pawn_png_128px.png"
            else:
                sprite = "sprites\\w_pawn_png_128px.png"

        piece = Piece(squares[squareIndex], types[i], team, sprite) 
        pieces.append(piece) #Add piece to list of pieces to return
        piece.getSquare().setPiece(piece) #Assign piece to square location within square object that is holding the piece
        squareIndex += 1
    return pieces
#Handle move decision for any pawn piece
def pawnMovement(possibleMoves, team, squares, square):
    if team == 1: #Set direction pawn can move in on the y axis.
        direction = -1
    else:
        direction = 1

    xaxis = square.getAxis()[0] #Get the board location of the piece
    
    yaxis = square.getAxis()[1]
    firstMove = square.getPiece().getFirst()
    #Gets the index of x and y axis in yaxislist and xaxislist
    xy = getAxis(xaxis, yaxis)
    #Variable for deciding if a pawn can move 2 at once.
    blocked = True
    #look through squares list for possible moves

    #Moving straight forward. . .
    inFront = squares[squaredex + (8*direction)]
    if inFront.getOccupied() == False: #Check if the piece in front is occupied
        possibleMoves.append(inFront)
        if square.getPiece().getFirst() == True: #Check if this is the pawns first move...
            doubleStep = squares[squaredex + (16 *direction)] #Check if two pieces in front is occupied
            if doubleStep.getOccupied() == False:
                possibleMoves.append(doubleStep)
   #Killing another piece. . .
    diagList = []
    if xaxis != 'A' and xaxis != "H": #Make sure that each team does not attempt to attack off the board, respectively
        diagList.append(squares[squaredex + (7*direction)])
        diagList.append(squares[squaredex + (9*direction)])
    elif xaxis == 'A':
        if team == 1:
            diagList.append(squares[squaredex + (7*direction)])
        else:
            diagList.append(squares[squaredex + (9*direction)])
    elif xaxis == "H":
        if team == 0:
            diagList.append(squares[squaredex + (7*direction)])
        else:
            diagList.append(squares[squaredex + (9*direction)])

    for square in diagList:
        if square.getOccupied() == True:
            if square.getPiece().getTeam() != team:
                possibleMoves.append(square)
#Handle move decision for any rook piece
def rookMovement(possibleMoves, team, squares, square):
    """
    Casle rules: Can move in any direction as long as it isnt diaganal or blocked by a piece.
    """
    #Check four directions in order.
    xaxis = square.getAxis()[0] #Get the board location of the piece
    yaxis = square.getAxis()[1]

    #Check upward movement. . . 
    upY = squaredex
    #Make sure piece isn't on top before checking if it can move upwards
    if squares[squaredex].getAxis()[1] != 8:
        while True:
            if squares[upY - 8].getOccupied() == False:
                possibleMoves.append(squares[upY - (8)])
                if squares[upY - 8].getAxis()[1] == 8:
                    break
                upY = upY - 8
            else:
                if squares[upY - (8)].getPiece().getTeam() != currentPlayer:
                    possibleMoves.append(squares[upY - (8)])
                break
            

    #Check Downward Movement
    downY = squaredex
    if squares[squaredex].getAxis()[1] != 1:
            while True:
                if squares[downY + (8)].getOccupied() == False:
                    possibleMoves.append(squares[downY + (8)])
                    if squares[downY + 8].getAxis()[1] == 1:
                        break
                    downY = downY + 8
                else:
                    if squares[downY + (8)].getPiece().getTeam() != currentPlayer:
                        possibleMoves.append(squares[downY + (8)])
                    break

    rightX = squaredex
    if squares[squaredex].getAxis()[0] != "H":
            while True:
                if squares[rightX + (1)].getOccupied() == False:
                    possibleMoves.append(squares[rightX + (1)])
                    if squares[rightX + 1].getAxis()[0] == "H":
                        break
                    rightX = rightX + 1
                else:
                    if squares[rightX + (1)].getPiece().getTeam() != currentPlayer:
                        possibleMoves.append(squares[rightX + (1)])
                    break
    leftX = squaredex
    if squares[squaredex].getAxis()[0] != "A":
            while True:
                if squares[leftX - 1].getOccupied() == False:
                    possibleMoves.append(squares[leftX - (1)])
                    if squares[leftX - 1].getAxis()[0] == "A": #Stop if on the edge you are moving towards
                        break
                    leftX = leftX - 1
                else:
                    if squares[leftX - 1].getPiece().getTeam() != currentPlayer:
                        possibleMoves.append(squares[leftX - 1])
                    break

def movepiece(currentSquare, futureSquare):
    currentPiece = currentSquare.getPiece() #The piece that will be moving
    if futureSquare.getOccupied() == True:
        toKill = futureSquare.getPiece()
        toKill.die() #Kill piece (remove from board)
    currentPiece.setSquare(futureSquare) #Assign the new square to the piece for drawing
    futureSquare.setPiece(currentPiece) #Assign piece to square for logic
    currentSquare.removePiece()
    currentPiece.pawnMoved()


    
    


#Setting global lists
squares = initSquares() #squares is where all the squares are stored in a list
pieces = initPieces(squares) #This is where all of the pieces are stored.
storedSquares = [0] #A list with the currently selected square and the previously selected square.
possibleMoves = []
currentPlayer = 1 #sets starting player, 1 is white to start, 0 is black.
squaredex = None #Index of currently selected square

#Start Progam. . . 
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    #This section is used to set the hover color for squares, and to select squares.
    for i, square in enumerate(squares):
        squareRect = pygame.Rect(square.getPos()[0], square.getPos()[1], 50, 50)
        #Check if mouse over square
        if squareRect.collidepoint(pygame.mouse.get_pos()):
            square.hover()


            if squareRect.collidepoint(pygame.mouse.get_pos()): #if you click on a square  #gets stored square
                if event.type == pygame.MOUSEBUTTONDOWN:
                    time.sleep(.3) #Wait to avoid multiclick, this is chess after all
                    #Check if the square you are mousing over is movable. . .
                    if square in possibleMoves:
                        movepiece(storedSquares[0], square)
                        for square in squares: #Reset all board colors
                            square.unselect()
                        storedSquares = [0]
                        possibleMoves = [] #Reset possible moves
                        if currentPlayer == 1:
                            currentPlayer = 0
                        else:
                            currentPlayer = 1


                    elif storedSquares[0] != 0: #if there is already a square selected
                        if square.getOccupied() == True:
                            if square.getPiece().getTeam() == currentPlayer:
                                selectedSquare = square #Maybe store the square you last hovered on?
                                storedSquares.append(storedSquares[0]) #last square clicked on
                                storedSquares[0] = selectedSquare
                                squaredex = i #Save index of selected square
                    else:
                        if square.getOccupied() == True:
                            if square.getPiece().getTeam() == currentPlayer:
                                storedSquares[0] = square #For first click
                                squaredex = i #Save index of selected square

                    if storedSquares[0] != 0:
                        storedSquares[0].select()
                    if len(storedSquares) > 1: #if there are two stored squares, one selected and one to unselect
                        storedSquares[1].unselect()
                        storedSquares.pop() #forget about old stored square
        else:
            #Reset color once no longer hovering over square, or once a square is no longer selected.
            square.resetColor()
    
    #Add logic for deciding which moves a piece can make on any turn, 0 is rook, 1 is knight, 2 is bishop, 3 is queen, 4 is king, 5 is pawn.
    """
    1st: Get the type of piece that you select
    2nd: Look around, highlight and remember any spaces it can possibly move to.
    3rd: Delete any pieces that it moves onto and move the remembered piece
    """
    #Run through piece types, get list of possible moves/squares (possibleMoves)
    if storedSquares[0] != 0: #Make sure there is a square/piece selected
        selectedPiece = storedSquares[0].getPiece()
        pieceType = selectedPiece.getType()
        #Get all possible for rooks. . . 
        if pieceType == 0:
            rookMovement(possibleMoves, currentPlayer, squares, storedSquares[0])
        #Get possible pieces for Pawns. . . 
        if pieceType == 5:
            pawnMovement(possibleMoves, currentPlayer, squares, storedSquares[0])



    #Set colors for possible moves, remove after testing is complete!!!
    for square in possibleMoves:
        square.hover()


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("tan")

    # RENDER YOUR GAME HERE
    #Draw board squares
    for square in squares:
        pygame.draw.rect(screen, square.getColor(), pygame.Rect(square.getPos()[0], square.getPos()[1], 50, 50))

    for piece in pieces:
        if piece.getAlive() == True:
            screen.blit(piece.getImage(), (piece.getSquare().getPos()[0], piece.getSquare().getPos()[1]))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()