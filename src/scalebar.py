
#from tkinter import Frame, Tk, Label, LEFT, X #Listbox, BOTH, END, @UnusedImport
#from tkinter import *  # @UnusedWildImport
import tkinter as tk
from PIL import Image, ImageTk  # @Reimport
import os

class ScaleBar(tk.Frame):

    def __init__(self, parent=None, imagepath=".", temprange = (200,333), units = "K"):
        self.parent = parent
        tk.Frame.__init__(self, parent,  bd=0, pady=10, height=60)
        self.pack(fill=tk.X)
        
        self.low = temprange[0]
        self.high = temprange[1]
        self.units = units
        self.imgpath = os.path.abspath(imagepath)
        
        self.loadscaleimage()
        self.createWidget()
    
    def createWidget(self):
        self.label_scale_image_image()
        self.assembleScaleText(self.units)    

    
    def unitconvert(self,temp, unit="C"):
        if unit == "C":
            temp = temp - 273
                    
        elif unit == "F":
            temp = int((temp - 273)*9/5+32  )
        
        return temp
    
            
    def loadscaleimage(self):
        try:
            scaleimg = Image.open(self.imgpath, "r")
            
            self.img = scaleimg.resize((640,20), Image.NEAREST)
            self.tkpi = ImageTk.PhotoImage(self.img)
        except:
            print("scale did not load")
            self.parent.quit()
        
    def label_scale_image_image(self):
        self.scale_image = tk.Label(self, image=self.tkpi,bg="grey",bd=2,relief=tk.GROOVE)
        self.scale_image.pack(side=tk.TOP)
    
    def assembleScaleText(self,unit="K"):
        self.scale_text = tk.Frame(self, bg="",bd=0,  padx=50, pady=0)
        self.scale_text.pack(side=tk.TOP, fill=tk.X)
        
        high = self.unitconvert(self.high,unit)
        low = self.unitconvert(self.low,unit)
        
        r = high - low
        
        div = 10
        x = int(r/div)

        for i in range(div+1):
            self.label_text(str(low+x*i))
        
    def label_text(self, txt):
        scale_text = tk.Label(self.scale_text,text=txt)
        scale_text.pack(side = tk.LEFT, expand=1, fill=tk.X)
        scale_text.pack_propagate(0)
   
    '''
    def listbox_text(self):
        self.scale_list = Listbox(self)
        self.scale_list.pack(fill=X, expand =1)
        for i in range(20):
            self.scale_list.insert(END,str(i))
       ''
        
             
def show(folder):
    root = tk.Tk()
    app = ScaleBar(root, folder)
    #root.geometry("700x250")
    
    app.mainloop()
    try:
        root.destroy()
    except Exception:
        pass
    
#g = "..\\media\\scale.png"

#show(g) #'''
