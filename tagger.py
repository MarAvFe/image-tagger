#!/usr/bin/python
try:                         # In order to be able to import tkinter for
    from tkinter import *    # either in python 2 or in python 3
    from tkinter import messagebox
except ImportError:
    from Tkinter import *
    from Tkinter import tkMessageBox
from  PIL import ImageTk, Image
import os, shutil

WIDTH=800
HEIGHT=600

class GUI(Frame):

    def __init__(self, master=None):
        global WIDTH, HEIGHT
        self.wdir = ''
        self.wimg = ''
        self.working_image_index = 0

        Frame.__init__(self, master)
        w, h = WIDTH, HEIGHT
        self.imgWidth, self.imgHeight = WIDTH-50, HEIGHT-50
        master.minsize(width=300, height=300)
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
        master.bind('j', self.skip_image)
        master.bind('f', self.back_image)
        master.bind('<Configure>', self.on_resize)

        self.master = master

    def on_resize(self, event):
        self.imgWidth, self.imgHeight = self.master.winfo_width()-50, self.master.winfo_height()-50
        if self.image.width() != 0:
            self.updateImage(False)

    def set_working_dir(self):
        from tkinter import filedialog
        selected = filedialog.askdirectory()
        self.wdir = selected + '/' if not selected.endswith('/') else selected
        self.workfiles = self.getContents(self.wdir)
        ok = self.setupFolders()
        if not ok:
            raise Exception("cannot create tag folders")
        self.updateImage()

    def set_next_image(self, wasSolved):
        if wasSolved:
            i = self.working_image_index
            self.workfiles = self.workfiles[:i] + self.workfiles[i+1:]
        else:
            try:
                self.working_image_index = (self.working_image_index + 1) % len(self.workfiles)
            except ZeroDivisionError:
                messagebox.showinfo("Info", "Please select a folder with images")
            except Exception as e:
                print(e)
        self.updateImage()

    def keep_image(self, event=None):
        shutil.move(self.wdir+self.wimg, self.wdir+'keep/'+self.wimg)
        self.set_next_image(True)

    def delete_image(self, event=None):
        shutil.move(self.wdir+self.wimg, self.wdir+'delete/'+self.wimg)
        self.set_next_image(True)

    def skip_image(self, event=None):
        self.set_next_image(False)

    def back_image(self, event=None):
        self.set_next_image(False)

    def updateImage(self, new=True):
        if not new:
            img = self.fittableImage(self.tmpImg)
            self.image = ImageTk.PhotoImage(img)
        else:
            self.tmpImg = self.getNextImage()
            if self.tmpImg != None:
                img = self.fittableImage(self.tmpImg)
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
        try:
            if (img.width > self.imgWidth) or (img.height > self.imgHeight):
                if img.width > img.height:
                    ratio = self.imgWidth / img.width
                    newsize = (self.imgWidth, int(img.height * ratio))
                else:
                    ratio = self.imgHeight / img.height
                    newsize = (int(img.width * ratio), self.imgHeight)
                img = img.resize(newsize, Image.ANTIALIAS)
        except:
            pass
        return img

root = Tk()
root.geometry("800x600")
ui_path = StringVar()
app = GUI(master=root)
app.mainloop()
root.destroy()
