from Tkinter import *
import sim2d
import sim3d
import game
import maps
import random
import pygame

# code adapted from hack112 project and 112 website
# Purpose: UI for launch page and redirects to the different game modes
def init(data):
    data.startText = "Water Simulation"
    data.instruct = "Choose the Mode:"
    data.startText2 = "Created by: Andy Chen"
    data.font1 = ('Monaco', 40)
    data.font2 = ('Monaco', 15)
    data.font3 = ('Monaco', 80)
    data.font4 = ('Monaco', 25)
    data.enter = False
    rand = random.randint(0,4)
    data.lstMapsWater = maps.getWater(0)
    data.lstMapBlocks = maps.getBlock(0)
    data.bucketLoc = pygame.Rect(260, 560,80,80)

    # creates the triangles for selecting an option
    data.arrow3D = [(data.width/2 - 130, data.height/2 + 125),
                    (data.width/2 - 150, data.height/2 + 115),
                    (data.width/2 - 150, data.height/2 + 135)]
    data.arrowBuild = [(data.width/2 - 130, data.height/2 + 175),
                        (data.width/2 - 150, data.height/2 + 165),
                        (data.width/2 - 150, data.height/2 + 185)]
    data.arrowGame = [(data.width/2 - 130, data.height/2 + 225),
                        (data.width/2 - 150, data.height/2 + 215),
                        (data.width/2 - 150, data.height/2 + 235)]
    data.select = "3D Simulation"

def keyPressed(event, data, root):
    if event.keysym == "Down":
        if data.select == "3D Simulation":
            data.select = "Build Mode"
        elif data.select == "Build Mode":
            data.select = "Game Mode"
        else:
            data.select = "3D Simulation"
    if event.keysym == "Up":
        if data.select == "Build Mode":
            data.select = "3D Simulation"
        elif data.select == "Game Mode":
            data.select = "Build Mode"
        else:
            data.select = "Game Mode"
    if event.keysym == "Return":
        if data.select == "3D Simulation":
            root.destroy()
            sim3d.main()
        elif data.select == "Build Mode":
            root.destroy()
            sim2d.mainLoop()
        else:
            root.destroy()
            game.mainLoop(data.lstMapsWater,data.lstMapBlocks)

def redrawAll(canvas, data): #redraws the board
    drawStartScreen(data, canvas)

def drawStartScreen(data, canvas): #draws start screen
    canvas.create_rectangle(0,0,data.width,data.height,fill='DodgerBlue2')
    canvas.create_text(data.width/2, (data.height/2)-25,
                        text = data.startText, font=data.font1,
                        fill="white")
    canvas.create_text(data.width/2, (data.height)-20,
                        text = data.startText2, font=data.font2,
                        fill='white')
    canvas.create_text(data.width/2, (data.height/2)+75,
                        text = data.instruct, font=data.font1,
                        fill='white')
    canvas.create_text(data.width/2, (data.height/2)+125,
                        text = "3D Simulation", font=data.font4,
                        fill='white')
    canvas.create_text(data.width/2, (data.height/2)+175,
                        text = "Build Mode", font=data.font4,
                        fill='white')
    canvas.create_text(data.width/2, (data.height/2)+225,
                        text = "Game Mode", font=data.font4,
                        fill='white')
    if data.select == "3D Simulation":
        canvas.create_polygon(data.arrow3D, fill="white")
    elif data.select == "Build Mode":
        canvas.create_polygon(data.arrowBuild, fill="white")
    else:
        canvas.create_polygon(data.arrowGame, fill="white")


# code taken from 112 starter code

def run(width=800, height=800):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                            fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()
    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data, root)
        redrawAllWrapper(canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    redrawAllWrapper(canvas, data)
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    # and launch the app
    root.mainloop()  # blocks until window is closed

run()
