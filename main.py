from tkinter import *
import time
import cv2
from PIL import Image, ImageTk
import math

class StopWatch(Frame):
    """ Implements a stop watch frame widget. """
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.makeWidgets()

    def makeWidgets(self):
        """ Make the time label. """
        l = Label(self, textvariable=self.timestr, anchor='w', width=100, height=5)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=0, padx=0)

    def _update(self):
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def Start(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1
            show_frame()

    def Stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def Reset(self):
        """ Reset the stopwatch. """
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

def bearing():
    global faces
    global x
    global y
    try:
        for (x2,y2, w, h) in faces:
            xCord = x2+50
            yCord = y2+50
        relX = x-xCord
        relY = y-yCord

        angle = ((math.atan(abs(relX)/abs(relY)))*180)/math.pi
        if (relX > 0) and (relY >0):
            return angle
        elif (relX < 0) and (relY >0):
            return (360-angle)
        elif (relX > 0) and (relY <0):
            return (180-angle)
        elif (relX < 0) and (relY <0):
            return (180+angle)
        else:
            pass
    except:
        pass

def show_frame():
    global x
    global y

    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 1)
    speed = 3
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    global faces

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    try:
        if (bearing()>=  345) and (bearing()<= 15):
            x+=0
            y-=3*speed
        elif (bearing()>= 16) and (bearing()<= 45):
            x-=1*speed
            y-=2*speed
        elif (bearing()>= 46) and (bearing()<= 75):
            x-=2*speed
            y-=1*speed
        elif (bearing()>= 76) and (bearing()<= 105):
            x-=3*speed
            y+=0
        elif (bearing()>= 106) and (bearing()<= 135):
            x-=2*speed
            y+=1*speed
        elif (bearing()>= 136) and (bearing()<= 165):
            x-=1*speed
            y+=2*speed
        elif (bearing()>= 166) and (bearing()<= 195):
            x+=0
            y+=3*speed
        elif (bearing()>= 196) and (bearing()<= 225):
            x+=1*speed
            y+=2*speed
        elif (bearing()>= 226) and (bearing()<= 255):
            x+=2*speed
            y+=1*speed
        elif (bearing()>= 256) and (bearing()<= 285):
            x+=3*speed
            y+=0
        elif (bearing()>= 286) and (bearing()<= 315):
            x+=2*speed
            y-=1*speed
        elif (bearing()>=316) and (bearing()< 345):
            x+=1*speed
            y-=2*speed
    except:
        pass
    # Draw a rectangle around the faces

    for (x2, y2, w, h) in faces:
        if math.sqrt((x-(x2+50))*(x-(x2+50))+(y-(y2+50))*(y-(y2+50)))< 10:
            cv2.circle(frame, (x,y), 10, (255, 0, 0), 4)
            print("Ded")
        else:
            cv2.circle(frame, (x,y), 10, (0, 255, 0), 4)

    # for (x, y, w, h) in faces:
    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    # cv2.imshow('Video', frame)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

x=0
y=0

faces = []

root = Tk() #gui
root.title('hack-shef')

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

imageFrame = Frame(root, width=300, height=400) #graphics
imageFrame.place(x=75, y=50)

sw = StopWatch(root)
sw.place(x=50, y=10)
root.geometry('800x600')
startButton = Button(root, text='Start', command=sw.Start)
startButton.place(x=600,y=25)
resetButton = Button(root, text='Reset', command=sw.Reset)
resetButton.place(x=650,y=25)
quitButton = Button(root, text='Quit', command=root.quit)
quitButton.place(x=700,y=25)

lmain = Label(imageFrame)
lmain.grid(row=0, column=0)
video_capture = cv2.VideoCapture(0)
root.mainloop() #start gui
