import sys
import turtle
import Tkinter as tkinter

class CommonSignalEncodeClass:

    NONE = -1
    HIGH = 0
    LOW = 1

    def __init__(self, rawTurtle, size, code, offsetX, offsetY):
        self.size = size
        self.code = code
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.rawTurtle = rawTurtle
        self.codeSplit = list(self.code)
        self.widthCount = len(self.codeSplit)
        self.titleTextOffset = 35
        self.codeTextOffset = 5
        self.textSize = 20
        self.signalType = "<None>"
        self.currentPosX = 0
        self.currentPosY = 0

    def drawBackground(self) :

        self.rawTurtle.color("red")
        self.rawTurtle.up()
        self.rawTurtle.goto(0+self.offsetX, self.size+self.titleTextOffset+self.offsetY);
        self.rawTurtle.write(self.signalType, move=False, align="left", font=("Arial", self.textSize, "normal"))
        self.rawTurtle.down()

        for j in range(self.widthCount):

            self.rawTurtle.color("black")
            self.rawTurtle.up()
            self.rawTurtle.goto(j*self.size+self.offsetX, self.size+self.codeTextOffset+self.offsetY);
            self.rawTurtle.write(self.codeSplit[j], move=False, align="left", font=("Arial", self.textSize, "normal"))

            self.rawTurtle.goto(j*self.size+self.offsetX,self.offsetY)
            self.rawTurtle.down()

            self.rawTurtle.color("light grey")
            for i in range(4):
                self.rawTurtle.forward(self.size)
                self.rawTurtle.left(90)

    def drawHighToRow(self) :

        if self.currentPosY != self.size + self.offsetY :
            self.rawTurtle.goto(self.currentPosX+self.offsetX, self.size+self.offsetY)

        self.rawTurtle.setheading(0)
        self.rawTurtle.forward(self.size/2)
        self.rawTurtle.right(90)
        self.rawTurtle.forward(self.size)
        self.rawTurtle.left(90)
        self.rawTurtle.forward(self.size/2)
        self.currentPosY = 0
        self.currentPosX += self.size

    def drawRowToHigh(self) :

        if self.currentPosY != 0 + self.offsetY :
            self.rawTurtle.goto(self.currentPosX+self.offsetX, 0+self.offsetY)

        self.rawTurtle.setheading(0)
        self.rawTurtle.forward(self.size/2)
        self.rawTurtle.left(90)
        self.rawTurtle.forward(self.size)
        self.rawTurtle.right(90)
        self.rawTurtle.forward(self.size/2)

        self.currentPosY = 1
        self.currentPosX += self.size

class ManchesterEncodeClass(CommonSignalEncodeClass):

    def __init__(self, rawTurtle, size, code, offsetX, offsetY):
        CommonSignalEncodeClass.__init__(self, rawTurtle, size, code, offsetX, offsetY)
        self.signalType = "<Manchester Encode>"

    def drawBackground(self):
        CommonSignalEncodeClass.drawBackground(self)


    def drawSignal(self):

        self.rawTurtle.up()

        self.rawTurtle.color("black")

        if (int)(self.codeSplit[0]) == 0 :
            self.currentPosY = 1
            self.rawTurtle.goto(0+self.offsetX, self.size+self.offsetY)
        else :
            self.currentPosY = 0
            self.rawTurtle.goto(0+self.offsetX, 0+self.offsetY)

        self.rawTurtle.down()

        for i in range(self.widthCount) :
            bit = (int)(self.codeSplit[i])

            if bit == 0 :
                self.drawHighToRow()
            else :
                self.drawRowToHigh()


class DifferentialManchesterEncodeClass(CommonSignalEncodeClass):

    def __init__(self, rawTurtle, size, code, offsetX, offsetY):
        CommonSignalEncodeClass.__init__(self, rawTurtle, size, code, offsetX, offsetY)
        self.signalType = "<DifferentialManchester Encode>"

    def drawBackground(self):
        CommonSignalEncodeClass.drawBackground(self)

    def drawSignal(self):

        self.currentPosY = 1
        self.rawTurtle.up()
        self.rawTurtle.goto(0+self.offsetX, self.size+self.offsetY);
        self.rawTurtle.color("black")

        self.rawTurtle.down()

        for i in range(self.widthCount) :
            bit = (int)(self.codeSplit[i])

            if bit == 0 :
                if self.currentPosY == 1 :
                    self.drawRowToHigh()
                else :
                    self.drawHighToRow()
            else :
                if self.currentPosY == 1 :
                    self.drawHighToRow()
                else :
                    self.drawRowToHigh()

if __name__ == "__main__":

    if len(sys.argv) != 3 or (sys.argv[1] != "1" and sys.argv[1] != "2" and sys.argv[1] != "3") :
        print "Usage : python main.py [signal type] [code]"
        print "--Signal Type--"
        print "1 : Manchester"
        print "2 : Differential Manchester"
        print "3 : Draw both"

    else :

        MANCHESTER = 1
        DIFFMANCHESTER = 2

        signalType = (int)(sys.argv[1])
        code = sys.argv[2]

        root = tkinter.Tk()
        root.geometry('1000x500-5+40') #added by me
        cv = turtle.ScrolledCanvas(root, width=1200, height=900)
        cv.pack()

        screen = turtle.TurtleScreen(cv)
        screen.screensize(2000,1000) #added by me
        t = turtle.RawTurtle(screen)
        t.hideturtle()

        t.speed(0)

        if signalType == MANCHESTER :
            signalClass = ManchesterEncodeClass(t,30,code,-250, 0)
            signalClass.drawBackground()
            signalClass.drawSignal()

        elif signalType == DIFFMANCHESTER:
            signalClass = DifferentialManchesterEncodeClass(t,30,code,-250, 0)
            signalClass.drawBackground()
            signalClass.drawSignal()

        else :
            signalClass1 = ManchesterEncodeClass(t,30,code,-250, 0)
            signalClass2 = DifferentialManchesterEncodeClass(t,30,code, -250 ,-100)

            signalClass1.drawBackground()
            signalClass1.drawSignal()

            signalClass2.drawBackground()
            signalClass2.drawSignal()

        root.mainloop()
