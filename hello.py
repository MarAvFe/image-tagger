#!/usr/bin/python
try:                        # In order to be able to import tkinter for
    from tkinter import *    # either in python 2 or in python 3
except ImportError:
    from Tkinter import *
from  PIL import ImageTk, Image

root = Tk()
root.title("Quick image picker")
root.geometry('800x600')
frame = Frame(root)
frame.pack()

WDIR = '/home/marcello/Documents/osource/quick-image-checker/img'
WIMG = '/test1.png'
ui_path = StringVar()


def getContents(dirname):
    import os
    images = []
    for file in os.listdir(dirname):
        if file[-3:] in ['png','jpg','gif']:
            images.append(file)
    return images

def working_dir():
    global WDIR, WORKFILES,img 
    from tkinter import filedialog
    WDIR = filedialog.askdirectory()
    ui_path.set('...'+WDIR[-50:] if len(WDIR)>50 else WDIR)
    print(WDIR)
    WORKFILES = getContents(WDIR)
    WIMG = WORKFILES[0]
    print(WIMG)
    root.update_idletasks()


def fittableImage(img):
    if (img.width > 750) or (img.height > 500):
        print(img.width, 'x', img.height)
        if img.width > img.height:
            ratio = 750 / img.width
            newsize = (750, int(img.height * ratio))
        else:
            ratio = 500 / img.height
            newsize = (int(img.width * ratio), 500)
        img = img.resize(newsize, Image.ANTIALIAS)
    return img
    


topFrame = Frame(frame)
topFrame.grid(column=0, row=0)

bottomframe = Frame(frame, bg='red')
bottomframe.grid(column=0, row=1)

pickPath = Button(topFrame, text="Pick folder", command=working_dir)
pickPath.pack(side=LEFT)
pickPath.grid(column=2, row=0)
txt = Label(topFrame, textvariable=ui_path, width=50)
txt.grid(column=1, row=0)

img = Image.open('img/test.png')
img = fittableImage(img)
img = ImageTk.PhotoImage(img)
panel = Label(bottomframe, image=img)
panel.image = img
panel.pack(side=TOP)

buttonframe = Frame(bottomframe)
buttonframe.pack(side=BOTTOM, fill="both", expand=True)
keep = Button(buttonframe, text="(K)eep", fg="black")
keep.grid(column=0,row=0)
delete = Button(buttonframe, text="(D)elete", fg="black")
delete.grid(column=1,row=0)

def loopCapture():
    img = Image.open((WDIR+'/' if not WDIR.endswith('/') else WDIR) + WIMG)
    img = fittableImage(img)
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)
    panel.img = img
    root.update_idletasks()
    root.after(500, loopCapture)

root.bind(500, loopCapture)
root.mainloop()
