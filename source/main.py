# import required libraries
from tkinter import *
from random import randint


class Game:
    # initialize variables
    fruit = False
    boardSize = 8
    headX = headY = dirX = dirY = 0
    bodyPeicesX = []
    bodyPeicesY = []
    fruitX = 0
    fruitY = 0
    initLength = 3
    counter = 0
    
    # calls once when class object is constructed
    def __init__(self, master):
        # bind keys w, a, s, and d to corresponding funcs
        master.bind('w', self.w)
        master.bind('a', self.a)
        master.bind('s', self.s)
        master.bind('d', self.d)
        # begin game loop
        self.gameLoop(master)

    # gets all widgets in inputted tkinter window and returns them in a list
    def allChildren(self, master):
        # get all widgets in master (tkinter window)
        list = master.winfo_children()
        # add all items in master to a list and return it
        for item in list:
            if item.winfo_children():
                list.extend(item.winfo_children())
        return list


    # TODO change func name to be more clear
    # loops the snake to the other side of the screen if it hits one edge
    def loop(self):
        if self.headX > self.boardSize-1:
            self.headX = 0
        if self.headY > self.boardSize-1:
            self.headY = 0
        if self.headX < 0:
            self.headX = self.boardSize-1
        if self.headY < 0:
            self.headY = self.boardSize-1

    
    # deletes body x and y at index 0
    def delBody(self):
        del self.bodyPeicesX[0]
        del self.bodyPeicesY[0]

    
    # calculates new head pos based on input dir
    def updateHeadPos(self):
        # adds current head pos to body pos list before moving
        self.bodyPeicesX.append(self.headX)
        self.bodyPeicesY.append(self.headY)
        # adds dir to body pos
        self.headX += self.dirX
        self.headY += self.dirY
        # calls loop() to loop snake around edge of the screen if head pos exceeds board size
        self.loop()
        if self.counter > self.initLength-1: 
            if self.headX == self.fruitX and self.headY == self.fruitY:
                self.fruit = False
            else:
                self.delBody()
        else: 
            self.counter += 1

    # deletes all widgets from a list returned by allChildren
    def deleteAllWidgets(self, master):
        # gets all widgets in master with allChildren
        widget_list = self.allChildren(master)
        # iterates through all items in list and deletes with the tkinter delete() function
        for item in widget_list:
            item.destroy()

    # renders board var to the screen
    def displayBoard(self, board, master):
        # delete all widgets to stop memory leak from widgets being overlayed but lower layers not being deleted
        self.deleteAllWidgets(master)
        # iterates through all board positions and renders it to the corresponding column and row with a label displaying a letter for what is there
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                Label1 = Label(master, text=board[i][j])
                Label1.grid(row=i, column=j)

    # generates a new fruit pos if fruit is not currently present and stores it in global vars fruitX and fruitY
    def genFruit(self):
        # TODO stop generating within body or at head pos
        # * for graphics, rotate head based on dir
        if not self.fruit:
            self.fruitX = randint(0, self.boardSize-1)
            self.fruitY = randint(0, self.boardSize-1)
        self. fruit = True

    # generates board to be rendered by displayBoard() - this func is the root of all the snake logic and rendering
    # TODO optimize func to use less iterations - just iterate through boyPieces and add them to board 
    def updateBoard(self, master):
        # self explanetory, updates head pos with updateHeadPos()
        self.updateHeadPos()
        # TODO check for head and body collision
        # create a array with size equal to var boardSize
        board = [[" "]*self.boardSize for i in range(self.boardSize)]
        # calls genFruit() to get a new fruit pos and adds it to board
        self.genFruit()
        board[self.fruitX][self.fruitY] = "F"
        # add all body positions and head pos to board
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                for k in range(len(self.bodyPeicesX)):
                    if i == self.bodyPeicesX[k] and j == self.bodyPeicesY[k]:
                        board[i][j] = "B"
                if self.headX == i and self.headY == j:
                    board[i][j] = "H"
        # pass generated board to displayBoard for rendering
        self.displayBoard(board, master)

    def gameLoop(self, master):
        self.updateBoard(master)
        # calls itself every 500 milliseconds
        master.after(500, lambda: self.gameLoop(master))

    # funcs that are bound to input w, a, s, and d
    def a(self, _event=None):
        self.dirY = -1
        self.dirX = 0

    def w(self, _event=None):
        self.dirX = -1
        self.dirY = 0

    def d(self, _event=None):
        self.dirY = 1
        self.dirX = 0

    def s(self, _event=None):
        self.dirX = 1
        self.dirY = 0

# init Tk instance
root = Tk()
# init game class instance
GameInstance = Game(root)
# call tkinter loop
root.mainloop()
