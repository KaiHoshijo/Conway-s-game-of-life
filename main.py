import pygame
from pygame.locals import *
import copy

# creating the game model
pygame.init()

# setting up the canbas
screen = pygame.display.set_mode((500, 500))
# getting the frame rate of the canvas
clock = pygame.time.Clock()
# setting the name of canvas
pygame.display.set_caption("Conway's Game of Life")
# setting up the font for the game
font = pygame.font.Font(None, 36)

# size of screen
screenWidth = screen.get_width()
screenHeight = screen.get_height()
print(screenWidth, screenHeight)

# get the distance between each vertical line
distanceBetweenWidth = screenWidth // 20
# get the distance between each horizontal line
distanceBetweenHeight = screenHeight // 20
print(distanceBetweenHeight, distanceBetweenWidth)

# range of the width of the  rectangles
rangeWidth = range(0, screenWidth-distanceBetweenWidth, distanceBetweenWidth)
# range of the height of the rectangles
rangeHeight = range(0, screenHeight-distanceBetweenHeight, distanceBetweenHeight)
# width and height of rectangle
rectArea = (distanceBetweenWidth, distanceBetweenHeight)

# cell data
# colour of the cell
cellColour = pygame.Color(100, 100, 100)
# width of the cell
cellWidth = 3
# state of the cell (alive or dead)
cellState = False
# dictionary of points that coincede to a list of a cell rect, cell colour, cell width, and cell state
cells = {}

# filling cells with data
for distanceWidth in rangeWidth:
    for distanceHeight in rangeHeight:
        cellRect = pygame.Rect((distanceWidth, distanceHeight), rectArea)
        cells[(distanceWidth, distanceHeight)] = [cellRect, cellColour, cellWidth, cellState]

# finding the neighbours of a cell's position
def findNeighbours(cellPosition, cells):
    for newX in range(cellPosition[0] - rectArea[0], cellPosition[0] + 2 * rectArea[0], rectArea[0]):
        for newY in range(cellPosition[1] - rectArea[1], cellPosition[1] + 2 * rectArea[1], rectArea[1]):
            if (newX in rangeWidth and newY in rangeHeight and (newX, newY) != cellPosition):
                yield cells[(newX, newY)]

# setting the cell to a live state
def setAlive(cellPosition):
    cells[cellPosition][1] = pygame.Color(100, 100, 0)
    cells[cellPosition][3] = True

# setting the cell to a dead state
def setDead(cellPosition):
    cells[cellPosition][1] = pygame.Color(100, 100, 100)
    cells[cellPosition][2] = cellWidth
    cells[cellPosition][3] = False

# getting count of live cells from neighbours
def getCount(neighbours):
    return len(list(
        filter(
            lambda neighbour: neighbour[-1], 
            neighbours
        )
    ))
    
# the rules set by the ruleFunction
# returns true or false depending on what is desired
# this is used to set cells to live or dead
def rules(cellPosition, cells, ruleFunction):
    neighbours = findNeighbours(cellPosition, cells)
    aliveCount = getCount(neighbours)
    return ruleFunction(aliveCount)

# running the game 
def startGame():
    # a list of the cells that are alive and the nearby dead cells
    deadCellsNearLiveCells = []
    liveCells = []

    # finds all alive and nearby dead cells
    for cell in cells:
        # ensuring that the cell is alive
        if (cells[cell][-1]):
            # getting the neighbours of live cells
            neighbours = findNeighbours((cells[cell][0].x, cells[cell][0].y), cells)
            # filtering out all nearby live cells
            filteredNeighbours = list(
                filter(
                    lambda neighbour: not neighbour[-1], 
                    neighbours
                )
            )
            # appending all nearby dead cells that aren't in the list already
            deadCellsNearLiveCells += list(
                filter(
                    lambda neighbour: neighbour not in deadCellsNearLiveCells, 
                    filteredNeighbours
                )
            )
            # appending all live cells to the list
            liveCells.append(cells[cell])

    # creating a copy so that the 'master' cells list isn't affected until desired
    copyCells = copy.deepcopy(cells)

    # editing the 'master' cells list and bringing select cells to life
    # the rules for becoming alive
    # A cell can only become alive if it has exactly 3 neighbours by it
    # If it does then the cell will be brought to life
    deadCellsNearLiveCells = [setAlive((cell[0].x, cell[0].y)) for cell in
        list(
            filter(
                lambda cell: 
                    rules(
                        (cell[0].x, cell[0].y),
                        copyCells,
                        lambda alive: alive == 3
                    ),
                deadCellsNearLiveCells
            )
        )
    ]
    # editing the 'master' cells list and killing select cells
    # the rules for being alive
    # A cell can only be alive if it has 2 or 3 neighbours by it
    # If it doesn't meet this requirement then the cell is killed
    liveCells = [setDead((cell[0].x, cell[0].y)) for cell in 
        list(
            filter(
                lambda cell: 
                    rules(
                        (cell[0].x, cell[0].y), 
                        copyCells, 
                        lambda alive: alive not in [2,3]
                    ), 
                liveCells
            )
        )
    ]

# just a basic test for the application
setAlive((rectArea[0] * 4, rectArea[1] * 4))
setAlive((rectArea[0] * 3, rectArea[1] * 4))
setAlive((rectArea[0] * 2, rectArea[1] * 4))

# playable buttons
# state of the play button
playButton = False
# colour of the play button
playColour = pygame.Color(150, 100, 50)
# rect of the play button
playRect = pygame.Rect((distanceBetweenWidth, screenHeight - distanceBetweenHeight), rectArea)
# state of the stop button 
stopButton = False
# colour of the stop button
stopColour = pygame.Color(50, 100, 150)
# rect of the stop button
stopRect = pygame.Rect((distanceBetweenWidth * 3, screenHeight - distanceBetweenHeight), rectArea)
# state of the reset button
resetButton = False
# colour of the reset button
resetColour = pygame.Color(50, 150, 100)
# rect of the reset button
resetRect = pygame.Rect((distanceBetweenWidth * 5, screenHeight - distanceBetweenHeight), rectArea)

play = True
while play:
    # filling the screen
    screen.fill((23, 23, 23))

    # setting the frame rate
    clock.tick(10)

    for event in pygame.event.get():
        if (event.type == QUIT):
            # exiting the game if the quit button is pressed
            play = False
        elif (event.type == MOUSEBUTTONDOWN):
            # setting cells to alive or dead depending on where the player clicked
            # iterates through each cells and checks if the mouse position is above the rect
            # if it is then make the cell alive if it wasn't already
            # or kill the cell if the cell was already alive
            for cell in cells:
                mouseX, mouseY = pygame.mouse.get_pos()
                if (cells[cell][0].collidepoint(mouseX, mouseY) and not playButton):
                    if (not cells[cell][3]):
                        setAlive(cell)
                    else:
                        setDead(cell)

    # drawing the play, stop, and reset buttons
    pygame.draw.rect(screen, playColour, playRect)
    pygame.draw.rect(screen, stopColour, stopRect)
    pygame.draw.rect(screen, resetColour, resetRect)

    # enabling the buttons available
    # the first button moves forward one scene, can be held
    # the second button stops the game
    # the third button resets and stops the game
    if (pygame.mouse.get_pressed()[0]):
        mouseX, mouseY = pygame.mouse.get_pos()
        if (playRect.collidepoint(mouseX, mouseY)):
            playButton = True
            # print("Play!")
        elif (stopRect.collidepoint(mouseX, mouseY)):
            playButton = False
            # print("Stop!")
        elif (resetRect.collidepoint(mouseX, mouseY)):
            resetButton = True
            playButton = False
            # print("Reset!")

    # actually playing the game if playButton is true
    if (playButton):
        # actually start conway's game of life
        startGame()
        playButton = False

    # resetting the game if the player wants to
    if (resetButton):
        for cell in cells:
            setDead(cell)
        resetButton = False

    # setting up the basic board
    # drawing the board and applying edits to the 'master' cell list
    for cell in cells:
        cellRect, cellColour, cellWidth, cellState = cells[cell]
        if not cellState:
            pygame.draw.rect(screen, cellColour, cellRect, cellWidth)
        else:
            pygame.draw.rect(screen, cellColour, cellRect)

    # updating the screen
    pygame.display.flip()