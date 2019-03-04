#!/usr/bin/python
try:                         # In order to be able to import tkinter for
    from tkinter import *    # either in python 2 or in python 3
    from tkinter import messagebox
except ImportError:
    from Tkinter import *
    from Tkinter import tkMessageBox
from  PIL import ImageTk, Image
import os, shutil


class GUI(Frame):

    def __init__(self, master=None):
        self.wdir = ''
        self.wimg = ''
        self.working_image_index = 0

        Frame.__init__(self, master)
        w,h = 800, 600
        master.minsize(width=w, height=h)
        master.maxsize(width=w, height=h)
        self.pack()

        self.file = Button(self, text='Browse', command=self.set_working_dir)
        self.keep = Button(self, text='(K)eep', command=self.keep_image)
        self.delete = Button(self, text='(D)elete', command=self.delete_image)
        self.choose = Label(self, text="Choose path").pack()
        self.image = PhotoImage()
        self.label = Label(image=self.image)


        self.file.pack(side=LEFT)
        self.keep.pack(side=LEFT)
        self.delete.pack(side=LEFT)
        self.label.pack(side=TOP)

        master.bind('k', self.keep_image)
        master.bind('d', self.delete_image)

    def choose(self):
        ifile = tkFileDialog.askopenfile(parent=self,mode='rb',title='Choose a file')
        path = ifile.name

    def set_working_dir(self):
        from tkinter import filedialog
        selected = filedialog.askdirectory()
        self.wdir = selected + '/' if not selected.endswith('/') else selected
        self.workfiles = self.getContents(self.wdir)
        ok = self.setupFolders()
        if not ok:
            raise Exception("cannot create tag folders")
        self.updateImage()

    def set_next_image(self):
        self.working_image_index = (self.working_image_index + 1) % len(self.workfiles)
        self.updateImage()

    def keep_image(self, event=None):
        shutil.move(self.wdir+self.wimg, self.wdir+'keep/'+self.wimg)
        self.set_next_image()

    def delete_image(self, event=None):
        shutil.move(self.wdir+self.wimg, self.wdir+'delete/'+self.wimg)
        self.set_next_image()

    def updateImage(self):
        img = self.getNextImage()
        if img != None:
            img = self.fittableImage(img)
            self.image = ImageTk.PhotoImage(img)
        else:
            self.image = PhotoImage()
        self.label.configure(image=self.image)
        self.label.image=self.image

    def getNextImage(self):
        try:
            self.wimg = self.workfiles[self.working_image_index]
            img = Image.open(self.wdir + self.wimg)
        except IndexError:
            messagebox.showinfo("Error", "No images found in path: " + self.wdir)
            img = None
        except (FileNotFoundError):
            if (os.path.exists(self.wdir + 'keep/' + self.wimg)) or (os.path.exists(self.wdir + 'delete/' + self.wimg)):
                messagebox.showinfo("Done!", "Finished tagging")
            else:
                messagebox.showinfo("Error", "Something happened. Check the stacktrace.")
                raise Exception("Something happened")
            img = None
        print('next:', img)
        return img

    def setupFolders(self):
        tags = ['keep', 'delete']
        for folder in tags:
            fullPath = self.wdir+folder
            if not os.path.isdir(fullPath):
                try:
                    os.mkdir(fullPath)
                except:
                    return False
        return True


    def getContents(self, dirname):
        images = []
        for file in os.listdir(dirname):
            if file[-3:] in ['png','jpg','gif']:
                images.append(file)
        return images


    def fittableImage(self, img):
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

root = Tk()
ui_path = StringVar()
app = GUI(master=root)
app.mainloop()
root.destroy()
