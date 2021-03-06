# import required libraries
from math import ceil
from random import randint
from tkinter.font import Font
from tkinter.tix import Tk
from tkinter.ttk import Button, Label

from numpy import sqrt, square


class Snake:
    # initialize variables
    fruit = False
    headX = headY = dirX = dirY = 0
    bodyPeicesX = []
    bodyPeicesY = []
    fruitX = 0
    fruitY = 0
    counter = 0
    gameStarted = False
    gameOver = False
    highScore = 0
    myFont = None

    fontSize = 16
    fontWeight = "normal"
    fontFamily = "ubuntu"
    boardSize = 8
    speed = 500
    initLength = 3

    # calls once when class object is constructed
    def __init__(self, master):
        # bind keys w, a, s, and d to corresponding funcs
        master.bind('w', self.w)
        master.bind('a', self.a)
        master.bind('s', self.s)
        master.bind('d', self.d)
        # begin game loop
        self.gameLoop(master)
        # create the font
        self.myFont = Font(family=self.fontFamily, size=self.fontSize)

    # gets all widgets in inputted tkinter window and returns them in a list
    def allChildren(self, master):
        # get all widgets in master (tkinter window)
        list = master.winfo_children()
        # add all items in master to a list and return it
        for item in list:
            if item.winfo_children():
                list.extend(item.winfo_children())
        return list

    # loops the snake to the other side of the screen if it hits one edge
    def loopToOtherSideOfScreen(self):
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
        # calls loopToOtherSideOfScreen() to loop snake around edge of the screen if head pos exceeds board size
        self.loopToOtherSideOfScreen()
        # delete body pos at index zero if not on fruit
        if self.counter > self.initLength-1:
            if self.headX == self.fruitX and self.headY == self.fruitY:
                self.fruit = False
            else:
                self.delBody()
            if self.dirX != 0 or self.dirY != 0:
                self.gameStarted = True
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
                Label1.configure(font=self.myFont)

    # generates a new fruit pos if fruit is not currently present and stores it in global vars fruitX and fruitY
    def genFruit(self):
        if not self.fruit:
            self.fruitX = randint(0, self.boardSize-1)
            self.fruitY = randint(0, self.boardSize-1)
        if self.fruitX == self.headX and self.fruitY == self.headY:
            self.genFruit()
        for i in range(len(self.bodyPeicesX)):
            if self.fruitX == self.bodyPeicesX[i] and self.fruitY == self.bodyPeicesY[i]:
                self.genFruit()
        self.fruit = True

    # generates board to be rendered by displayBoard() - this func is the root of all the snake logic and rendering
    def updateBoard(self, master):
        # self explanetory, updates head pos with updateHeadPos()
        self.updateHeadPos()
        for i in range(len(self.bodyPeicesX)):
            if self.bodyPeicesX[i] == self.headX and self.bodyPeicesY[i] == self.headY and self.gameStarted:
                self.gameOver = True
        # create a array with size equal to var boardSize
        board = [["   "]*self.boardSize for i in range(self.boardSize)]
        # calls genFruit() to get a new fruit pos and adds it to board
        self.genFruit()
        # render fruit, body and then head
        board[self.fruitX][self.fruitY] = "F"
        for i in range(len(self.bodyPeicesX)):
            board[self.bodyPeicesX[i]][self.bodyPeicesY[i]] = "B"
        board[self.headX][self.headY] = "H"
        # pass generated board to displayBoard for rendering
        self.displayBoard(board, master)

    def gameLoop(self, master):
        self.updateBoard(master)
        # calls itself every 500 milliseconds
        if not self.gameOver:
            master.after(self.speed, lambda: self.gameLoop(master))
        else:
            self.restart(master)

    def restart(self, master):
        # reset variables
        self.deleteAllWidgets(master)
        self.fruit = False
        self.headX = self.headY = self.dirX = self.dirY = 0
        self.bodyPeicesY = []
        self.fruitX = 0
        self.fruitY = 0
        self.counter = 0
        self.gameStarted = False
        self.gameOver = False
        # display text on end screen
        if len(self.bodyPeicesX) > self.highScore:
            Label(master, text="You improved your highscore by: " +
                  str(len(self.bodyPeicesX)-self.highScore)).grid(row=0, column=0)
            Label(master, text="Your old highscore was: " +
                  str(self.highScore)).grid(row=4, column=0)
            self.highScore = len(self.bodyPeicesX)
        Label(master, text="Game over!").grid(row=1, column=0)
        Label(master, text="Your score was: " +
              str(len(self.bodyPeicesX))).grid(row=2, column=0)
        Label(master, text="Your highscore is: " +
              str(self.highScore)).grid(row=3, column=0)
        self.bodyPeicesX = []
        Button(master, text="Play again", command=lambda: self.gameLoop(
            master)).grid(row=5, column=0)

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

class Pong:
    boardSize = 8
    paddleSize = 3
    padding = 1
    dir = 0
    ballDirX = 0
    ballDirY = 0
    gameStarted = False
    gameOver = False
    highScore = 0
    myFont = None
    fontSize = 16
    fontWeight = "normal"
    fontFamily = "ubuntu"
    originX = 4
    originY = 4
    destX = 8
    destY = 12
    ballX = 0
    ballY = 0
    speed = 500
    i = 0
    
    def __init__(self, master):
        # bind keys w, a, s, and d to corresponding funcs
        master.bind('w', self.w)
        master.bind('s', self.s)
        self.gameLoop(master)
        self.myFont = Font(family=self.fontFamily, size=self.fontSize)
    
    def w(self):
        self.dir = 1
    
    def s(self):
        self.dir = -1
    
    # gets all widgets in inputted tkinter window and returns them in a list
    def allChildren(self, master):
        # get all widgets in master (tkinter window)
        list = master.winfo_children()
        # add all items in master to a list and return it
        for item in list:
            if item.winfo_children():
                list.extend(item.winfo_children())
        return list

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
        for i in range(self.boardSize+1):
            for j in range(self.boardSize+1):
                Label1 = Label(master, text=board[i][j])
                Label1.grid(row=j, column=i)
                Label1.configure(font=self.myFont)
                
    def generateBoard(self,master):
        board = [["   "]*15 for i in range(15)]  
        self.interpolate()
        if self.ballX == 8 or self.ballX == 0:
            self.destX = abs(self.ballX-8) + randint(-1,1)
            self.destY = abs(self.originY-8) + randint(-1,1)
            self.originX = self.ballX
            self.originY = self.ballY
            self.i = 1
        if self.ballY == 0 or self.ballY >= 8:
            self.originX = self.ballX
            self.originY = self.ballY
            self.destY = abs(self.ballY-8) + randint(-1,1)
            self.i = 1
        board[self.ballX][self.ballY] = "B"
        board[8][8] = "8"
        board[0][0] = "0"
        self.displayBoard(board,master)
    
    def interpolate(self):
        dis = round(sqrt(square(self.originX-self.destX)+square(self.originY-self.destY)))
        d = round((1-((dis-self.i)/dis)),2)
        self.ballX = round(abs(self.originX+(d*self.destX)-(d*self.originX)))
        self.ballY = round(abs(self.originY+(d*self.destY)-(d*self.originY)))
        print(self.destY)
        print(self.destY)
        if self.i < dis:
            self.i += 1
    
    def gameLoop(self, master):
        self.generateBoard(master)
        # calls itself every 500 milliseconds
        if not self.gameOver:
            master.after(self.speed, lambda: self.gameLoop(master))
        else:
            self.restart(master)

    def restart(self, master):
        pass

# init Tk instance
root = Tk()
# init game class instance
GameInstance = Snake(root)
# GameInstance = Pong(root)
# call tkinter loop
root.mainloop()
