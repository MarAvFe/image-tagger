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
HMARGIN=50
VMARGIN=60

class GUI(Frame):

    def __init__(self, master=None):
        global WIDTH, HEIGHT, HMARGIN, VMARGIN
        self.wdir = ''
        self.wimg = ''
        self.working_image_index = 0
        self.workfiles = []
        self.lastTags = []

        Frame.__init__(self, master)
        w, h = WIDTH, HEIGHT
        self.imgWidth, self.imgHeight = WIDTH-HMARGIN, HEIGHT-VMARGIN
        master.minsize(width=300, height=300)
        self.pack()

        self.browseBtn = Button(self, text='(B)rowse', command=self.set_working_dir)
        self.keepBtn = Button(self, text='(K)eep', command=self.keep_image)
        self.deleteBtn = Button(self, text='(D)elete', command=self.delete_image)
        self.nextBtn = Button(self, text='(J) Next', command=self.next_image)
        self.backBtn = Button(self, text='(F) Back', command=self.back_image)
        self.undoBtn = Button(self, text='(Z) Undo', command=self.undo_image)
        self.quitBtn = Button(self, text='(Q) Quit', command=self.quit)
        self.ui_path = StringVar()
        self.ui_path.set('Path: ')
        self.pathLbl = Label(self, textvariable=self.ui_path)
        self.image = PhotoImage()
        self.label = Label(image=self.image)

        self.pathLbl.pack()
        self.browseBtn.pack(side=LEFT)
        self.keepBtn.pack(side=LEFT)
        self.deleteBtn.pack(side=LEFT)
        self.nextBtn.pack(side=LEFT)
        self.backBtn.pack(side=LEFT)
        self.undoBtn.pack(side=LEFT)
        self.quitBtn.pack(side=LEFT)
        self.label.pack(side=TOP)

        master.bind('b', self.set_working_dir)
        master.bind('k', self.keep_image)
        master.bind('d', self.delete_image)
        master.bind('j', self.next_image)
        master.bind('f', self.back_image)
        master.bind('z', self.undo_image)
        master.bind('q', self.quit)
        master.bind('<Configure>', self.on_resize)

        self.master = master

    def on_resize(self, event):
        self.imgWidth, self.imgHeight = self.master.winfo_width()-HMARGIN, self.master.winfo_height()-VMARGIN
        if self.image.width() != 0:
            self.update_image(False)

    def set_working_dir(self, event=None):
        from tkinter import filedialog
        selected = filedialog.askdirectory()
        self.wdir = selected + '/' if not selected.endswith('/') else selected
        self.ui_path.set('Path: ' + self.wdir)
        self.workfiles = self.get_contents(self.wdir)
        self.workfiles.sort()
        ok = self.setup_folders()
        if not ok:
            raise Exception("cannot create tag folders")
        self.update_image()

    def keep_image(self, event=None):
        self.classify(True)

    def delete_image(self, event=None):
        self.classify(False)

    def next_image(self, event=None):
        self.move_index(False)

    def back_image(self, event=None):
        self.move_index(True)

    def undo_image(self, event=None):
        src, tag = self.retrieve_tag()
        if tag == '':
            return
        shutil.move(self.wdir+src+tag, self.wdir+tag)
        self.workfiles.insert(self.working_image_index, tag)
        self.update_image()

    def classify(self, keep):
        dst = 'keep/' if keep else 'delete/'
        self.save_tag(dst, self.wimg)
        shutil.move(self.wdir+self.wimg, self.wdir+dst+self.wimg)
        i = self.working_image_index
        self.workfiles = self.workfiles[:i] + self.workfiles[i+1:]
        if i == len(self.workfiles):  # If reached  the end, loop up
            self.move_index(False)
        else:
            self.update_image()

    def move_index(self, goBack):
        if len(self.workfiles) == 0:
            messagebox.showinfo("Info", "Please select a folder with images")
            return
        if goBack:
            self.working_image_index = (self.working_image_index - 1) % len(self.workfiles)
        else:
            self.working_image_index = (self.working_image_index + 1) % len(self.workfiles)
        self.update_image()

    def save_tag(self, dst, name):
        self.lastTags.append((dst, name))
        self.lastTags = self.lastTags[-10:]

    def retrieve_tag(self):
        if len(self.lastTags) == 0:
            messagebox.showinfo("Warning", "History limit reached!")
            return '', ''
        spliced, popped  = self.lastTags[:-1], self.lastTags[-1]
        self.lastTags = spliced
        return popped[0], popped[1]  # dst, tag

    def update_image(self, new=True):
        if not new:
            img = self.fittable_image(self.tmpImg)
            self.image = ImageTk.PhotoImage(img)
        else:
            self.tmpImg = self.get_next_image()
            if self.tmpImg != None:
                img = self.fittable_image(self.tmpImg)
                self.image = ImageTk.PhotoImage(img)
            else:
                self.image = PhotoImage()
        self.label.configure(image=self.image)
        self.label.image=self.image

    def get_next_image(self):
        if len(self.workfiles) == 0:
            messagebox.showinfo("Not Found", "No images found in path: " + self.wdir)
            img = None
        try:
            self.wimg = self.workfiles[self.working_image_index]
            img = Image.open(self.wdir + self.wimg)
            self.ui_path.set('Path: ' + self.wdir + self.wimg)
        except FileNotFoundError:
            if (os.path.exists(self.wdir + 'keep/' + self.wimg)) or (os.path.exists(self.wdir + 'delete/' + self.wimg)):
                messagebox.showsuccess("Done!", "Finished tagging")
            else:
                messagebox.showerror("Error", "Something happened. Check the stacktrace.")
                raise Exception("Something happened")
            img = None
        return img

    def setup_folders(self):
        tags = ['keep', 'delete']
        for folder in tags:
            fullPath = self.wdir+folder
            if not os.path.isdir(fullPath):
                try:
                    os.mkdir(fullPath)
                except:
                    return False
        return True


    def get_contents(self, dirname):
        images = []
        for file in os.listdir(dirname):
            if file[-3:] in ['png','jpg','gif']:
                images.append(file)
        return images


    def fittable_image(self, img):
        try:
            if img.width > self.imgWidth:
                ratio = self.imgWidth / img.width
                newsize = (self.imgWidth, int(img.height * ratio))
                img = img.resize(newsize, Image.ANTIALIAS)
            if img.height > self.imgHeight:
                ratio = self.imgHeight / img.height
                newsize = (int(img.width * ratio), self.imgHeight)
                img = img.resize(newsize, Image.ANTIALIAS)
        except:
            # If failed to resize, just return as is
            pass
        return img

    def quit(self, event=None):
        self.master.destroy()

try:
    root = Tk()
    root.geometry("800x600")
    app = GUI(master=root)
    app.mainloop()
    root.destroy()
except TclError:
    pass
