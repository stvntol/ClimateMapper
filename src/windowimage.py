
#from tkinter import Frame, Tk, Label, Button  # @UnusedImport
import tkinter as tk
from PIL import Image, ImageTk
import os

mandelbrot = "C:\\Users\\Flocko\\Pictures\\Madelbrot\\360"
maps = 'C:\\Users\\Flocko\\Pictures\\maps\\Torr\\construction'
grid = 'C:\\Users\\Flocko\\workspace\\pyClim\\sandbox\\img'


class ImageViewer(tk.Frame):

    def __init__(self, parent=None, imagedir = grid):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.pack()
        
        self.imgpath = imagedir
        self.scrolling = False
         
        self.piclist()
        self.pic()
       
        self.createWidget()
        #self.poll()
        

    def piclist(self):
        # creates a list of all .png files in the directory
        
        dirlist = os.listdir(path=self.imgpath)
        self.imglist =[]
        for item in dirlist:
            if item[-3:] == "png":
                self.imglist.append(item)
        if len(self.imglist) == 0:
            print("No png images found in directory")
            self.parent.destroy()
            #this doesn't work as intended
        else:
            self.imglist.sort()
            self.imgnumber = 0
            self.imgnumber_old = 0
    
    def createWidget(self):
        self.buttons = tk.Frame(self)
        self.buttons.pack()
        
        self.button_prev()
        self.button_next()
        self.button_scroll()
        
        self.label_imgnumber()
        self.label_pic()        
        
    def pic(self):
        #loads an image from self.imglist. Resizes images to fit window.
        #creates self.img and self.tkpi for use by tkinter
        
        imgloc = os.path.join(self.imgpath,self.imglist[self.imgnumber])
        try:
            uimg = Image.open(imgloc, "r")
            w = uimg.size[0]
            h = uimg.size[1]
            ratio = w/h
            
            if h > 1000 or w > 1000:
                if h > w:
                    height = 1000
                else:
                    height = int(1000/ratio)
            elif h < 200 or w <200:
                height = 400
            else:
                height = h
                
            self.img = uimg.resize((int(height*ratio),height), Image.NEAREST)
            self.tkpi = ImageTk.PhotoImage(self.img)
       
        except FileNotFoundError as e:
            print(e)
            print(self.imglist[self.imgnumber], "will be removed from list.")
            self.imglist.pop(self.imgnumber)   
            self.imgnumber -= 1
    
    def label_pic(self):
        #tkinter Label: holds the image and displays it.
        self.label_image = tk.Label(self,image = self.tkpi)
        #self.label_image.place(x=0, y=0, width=self.img.size[0], height = self.img.size[1])
        self.label_image.pack()

    def label_imgnumber(self):
        self.imgnum_label = tk.Label(self, text = self.imglist[self.imgnumber])
        self.imgnum_label.pack()

    def button_next(self):
        #tkinter Button: executes self.button_next_act
        self.next_button = tk.Button(self.buttons)
        self.next_button["text"] = "Next",
        self.next_button["command"] = self.button_next_act
        self.next_button.pack(side=tk.LEFT)
    
    def button_next_act(self):
        #changes self.img and self.tkpi to the next image on self.imglist
        self.imgnumber =  (self.imgnumber + 1) % len(self.imglist)
          
        
    def button_prev(self):
        #tkinter Button: executes self.button_prev_act
        self.prev_button = tk.Button(self.buttons)
        self.prev_button["text"] = "Previous",
        self.prev_button["command"] = self.button_prev_act
        self.prev_button.pack(side=tk.LEFT)
                         
    def button_prev_act(self):
        #changes self.img and self.tkpi to the previous image on self.imglist
        self.imgnumber =  (self.imgnumber - 1) % len(self.imglist)
        
    
    def button_scroll(self):
        self.scroll_button = tk.Button(self.buttons)
        self.scroll_button["text"] = "Scroll",
        self.scroll_button["command"] = self.button_scroll_act
        self.scroll_button.pack(side=tk.LEFT)
    
    def button_scroll_act(self):
        if self.scrolling == False:
            self.scrolling = True
            self.scroll_button.configure(text="STOP")
        else:
            self.scrolling = False
            self.imgnumber_old = self.imgnumber
            self.scroll_button.configure(text="Scroll")
        
    def poll(self):      
        if self.imgnumber != self.imgnumber_old:
            self.pic()
            self.label_image.configure(image = self.tkpi)
            self.imgnum_label.configure(text = self.imglist[self.imgnumber])
            self.imgnumber_old = self.imgnumber
        if self.scrolling == True:
            self.button_next_act()
        self.parent.after(1000//60, self.poll)
        
'''
def show(folder=grid):
    root = Tk()
    app = ImageViewer(root, folder)
    root.geometry("1000x600")
    
    app.mainloop()
    try:
        root.destroy()
    except Exception:
        pass
        '''


