"""
Welcome to my chess program!

Here is a link to the spritework that I used... https://opengameart.org/content/chess-pieces-and-board-squares
"""

import pygame
import time
WIDTH = 500
HEIGHT = 600
WHITE = pygame.Color("#f8f3f1")
BLACK = pygame.Color("#4e3023")
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

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

    def getAxis(self):
        return f"{self.xaxis}{self.yaxis}"

    def getOccupied(self):
        return self.occupied
    
    def select(self):
        self.selected = True
    def unselect(self):
        self.selected = False
    def getSelected(self): #Get whether the square is selected
        return self.selected
    
    
class Piece:
    def __init__(self, square, type, team, image):
        self.square = square
        self.type = type
        self.team = team
        self.image = pygame.image.load(image)
    def move(self, newSquare): #Move to new square
        self.square = newSquare

    def die(self): #Unlink the piece from the square
        self.square = None

    def getImage(self):
        return self.image

    def getSquare(self):
        return self.square


#Init all of the square objects for the board
def initSquares():
    squares = []
    xaxisList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    yaxisList = [8, 7, 6, 5, 4, 3, 2, 1]
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
squares = initSquares() #squares is where all the squares are stored in a list

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
pieces = initPieces(squares) #This is where all of the pieces are stored.

storedSquares = [0] #A list with the currently selected square and the previously selected square.
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    #This section is used to set the hover color for squares
    for square in squares:
        squareRect = pygame.Rect(square.getPos()[0], square.getPos()[1], 50, 50)
        #Check if mouse over square
        if squareRect.collidepoint(pygame.mouse.get_pos()):
            square.hover()

            if squareRect.collidepoint(pygame.mouse.get_pos()): #if you click on a square
                if event.type == pygame.MOUSEBUTTONDOWN:
                    time.sleep(.1)
                    print(len(storedSquares))
                    if storedSquares[0] != 0: #if there is already a square selected
                        selectedSquare = square #Maybe store the square you last hovered on?
                        storedSquares.append(storedSquares[0]) #last square clicked on
                        storedSquares[0] = selectedSquare
                    else:
                        storedSquares[0] = square #For first click
                        print("should have")
                
                    storedSquares[0].select()
                    if len(storedSquares) > 1: #if there are two stored squares, one selected and one to unselect
                        print("reset")
                        storedSquares[1].unselect()
                        storedSquares[1].resetColor()
                        print(f"stored axis {storedSquares[1].getAxis()}")
                        storedSquares.pop() #forget about old stored square

        else:
            #Reset color once no longer hovering over square
            square.resetColor()
        

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("tan")

    # RENDER YOUR GAME HERE
    #Draw board squares
    for square in squares:
        pygame.draw.rect(screen, square.getColor(), pygame.Rect(square.getPos()[0], square.getPos()[1], 50, 50))

    for piece in pieces:
        screen.blit(piece.getImage(), (piece.getSquare().getPos()[0], piece.getSquare().getPos()[1]))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()