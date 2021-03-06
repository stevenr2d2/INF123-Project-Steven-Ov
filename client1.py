from network import Handler, poll
import sys
from threading import Thread
from time import sleep

import pygame
from pygame.locals import *

# refresh the game board on the screen
def showBoard (BoardViewingContainer, board):
    BoardViewingContainer.blit (board, (0,0))
    pygame.display.flip()
    
#detect where user clicks
def boardPos (mouseX, mouseY):
    # determine the column the user clicked
    if (mouseX < 100):
        col = 0
    elif (mouseX < 200):
        col = 1
    else:
        col = 2
    # row the user clicked
    if (mouseY < 100):
        row = 0
    elif (mouseY < 200):
        row = 1
    else:
        row = 2
    #return the row/column that the user clicked
    return (row, col)

#method to take action when user clicks board and determine where we want to
#place the x and o

def drawMove (board, boardRow, boardCol, Piece):
    # draw an X or O (Piece) on the board at boardRow, boardCol
    # determine the center of the space 

    # (this works because our spaces are 100 pixels wide and the first one

    #  is numbered zero)

    centerX = boardCol * 100 + 50

    centerY = boardRow * 100 + 50

    # draw the the "X" or "O" on the board
    if (Piece == 'X'):
        pygame.draw.line (board, (0,0,0), (centerX - 22, centerY - 22),(centerX + 22, centerY + 22), 2)
        pygame.draw.line (board, (0,0,0), (centerX + 22, centerY - 22), (centerX - 22, centerY + 22), 2)

    else:
        pygame.draw.circle (board, (0,0,0), (centerX, centerY), 44, 2)
 

    # store the board piece in the array so we can decide if there is a piece there and also to determine who the winner is.
    GameGrid[boardRow][boardCol] = Piece

#function to check board and see if there is a winner
def CheckIfWinner(board):

    # ask python for me to access these global variables
    global gameLoopBoolean, GameGrid

    # check if all values are equal for columns
    for col in range (0, 3):
        if (GameGrid[0][col] is not None) and (GameGrid[0][col] == GameGrid[1][col] == GameGrid[2][col]):
            print GameGrid[0][col] + " is the winner"
            print "Game Over"
            gameLoopBoolean = False #break the game loop
            break
        
    # check for winning rows
    for row in range (0, 3):

    #check if all the values are equal for all the rows
        if (GameGrid [row][0] is not None) and (GameGrid [row][0] == GameGrid[row][1] == GameGrid[row][2]):
            print GameGrid[row][0] + " is the winner"
            print "Game Over"
            gameLoopBoolean = False
            break #break the game loop

    # check if all values are equal for the diagonals
    if (GameGrid[0][0] == GameGrid[1][1] == GameGrid[2][2]) and (GameGrid[0][0] is not None):
        print GameGrid[0][0] + " is the winner"
        print "Game Over"
        gameLoopBoolean = False

    if (GameGrid[0][2] == GameGrid[1][1] == GameGrid[2][0]) and (GameGrid[0][2] is not None):
        print GameGrid[0][2] + " is the winner"
        print "Game Over"
        gameLoopBoolean = False

    
# make empty grid 3x3 so i can use to determine state of the game
GameGrid =  [[None, None, None],[None, None, None],[None, None, None]]

# By default X will go first
# Start Initalizing global variables here
PlayerGlobal = 'X'
pygame.init()
BoardViewingContainer = pygame.display.set_mode((300,300))
gameLoopBoolean = True
board_changed = False

backgroundLines = pygame.Surface (BoardViewingContainer.get_size())
backgroundLines = backgroundLines.convert()
backgroundLines.fill ((250,250,250))
# Make horizontal and vertical lines on the grid
pygame.draw.line (backgroundLines, (0,0,0), (0,100), (300,100), 2)
pygame.draw.line (backgroundLines, (0,0,0), (0,200), (300,200), 2)
pygame.draw.line (backgroundLines, (0,0,0), (100,0), (100,300), 2)
pygame.draw.line (backgroundLines, (0,0,0), (200,0), (200,300), 2)

board = backgroundLines

#Do this so that the board does not show up black
BoardViewingContainer.blit (board, (0,0))
pygame.display.flip()
# END Initalizing global variables here

# will use for networking will prompt user on start up in the future
FirstPlayerName = ""
SecondPlayerName = ""


myname = raw_input('What is your name? ')
playerCharacterJustWent = ""
row_justClicked = ""
col_justClicked = ""

class Client(Handler):
    
    def on_close(self):
        pass
    
    def on_msg(self, msg):
	global playerCharacterJustWent, row_justClicked, col_justClicked, PlayerGlobal, board_changed
        if 'txt' in msg:
            print msg['txt']
	if 'updateGameBoard' in msg:
	    print msg['updateGameBoard'] + " " + msg['row_clicked'] + " " + msg['col_clicked']
	    playerCharacterJustWent = msg['updateGameBoard']
  	    row_justClicked = msg['row_clicked'] 
	    col_justClicked = msg['col_clicked'] 


            continueFlag = True

	    row = int(row_justClicked) 
	    col = int(col_justClicked ) 
            # make sure this space isn't used
            if ((GameGrid[row][col] == 'X') or (GameGrid[row][col] == 'O')):
            # return nothing and end the function because the space grid location is occupied
                continueFlag = False
            if continueFlag == True:
                # draw an X or O
                ##    drawMove (board, row, col, PlayerGlobal)
		##convert them to int
	        print row_justClicked
		print col_justClicked

                drawMove (board, row, col, PlayerGlobal)
                ##    drawMove (board, int(row_justClicked), int(col_justClicked), PlayerGlobal)

##playerCharacterJustWent = ""

                    # set the other players turn
                if (PlayerGlobal == 'O'):
                    PlayerGlobal = 'X'
                    board_changed = True # use these flags because it will be handy in the future
                else:
                    PlayerGlobal = 'O'
                    board_changed = True # use these flags because it will be handy in the future
                # check for a winner
                CheckIfWinner(board)            
            if board_changed:
            # update the display
               showBoard (BoardViewingContainer , board)
               board_changed = False
        
host, port = '169.234.5.152', 8887
client = Client(host, port)
client.do_send({'join': myname})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
                            
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()




while 1:
##    try:
##        mytxt = sys.stdin.readline().rstrip()
##        client.do_send({'speak': myname, 'txt': mytxt})
##    except KeyboardInterrupt:
##        client.do_send({'speak': myname, 'txt': 'close'})
##        print "Client Shutdown Complete..."
##        sys.exit()
        for event in pygame.event.get():
            if event.type is QUIT:
                 gameLoopBoolean = False
            elif event.type is MOUSEBUTTONDOWN and gameLoopBoolean is True:
                # check if a user clicked on the board

                (mouseX, mouseY) = pygame.mouse.get_pos()
                (row, col) = boardPos (mouseX, mouseY)

                client.do_send({'row_clicked': str(row),'col_clicked': str(col),'speak': "Client 1 Row Clicked", 'txt': str(row)})


    
