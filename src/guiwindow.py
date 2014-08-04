
import windowimage, scalebar
#from tkinter import Frame, Tk
import tkinter as tk
import os

grid = 'C:\\Users\\Flocko\\workspace\\pyClim\\sandbox\\img'
g = "..\\images\\scale.png"

class ParentGUI(tk.Frame):
    
    def __init__(self, parent=None, imagedir = grid, scaledir = g, temprange = (200,333), units = "K"):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.parent.title("Climate")
        self.imgview = windowimage.ImageViewer(self, imagedir)
        
        if os.path.exists(scaledir):
            self.scale = scalebar.ScaleBar(self,scaledir, temprange, units)
        else:
            self.scale = scalebar.ScaleBar(self,g, temprange , units = "K")
            print("FAILURE! Could not locate desired scale image")
        
        self.pack()
        
        self.imgview.poll()
            
def show(folder=grid, temprange = (200,333), units = "K"):
    root = tk.Tk()
    
    scaledir = os.path.join(folder,"scale\\scale.png")
    app = ParentGUI(root, folder, scaledir, temprange, units)
    #root.geometry("1000x600")
    
    app.mainloop()
    try:
        root.destroy()
    except Exception:
        pass



if __name__ == "__main__":
    
    x = os.path.abspath(os.path.join("../media","Why Not 3650days 82x41 20140324 211159"))
    y = os.path.abspath(os.path.join("../media","Axial Tilt 3650days 82x41 20140403 022056"))
    
    show(y, temprange=(213,340),units="C")

'''    
print()
 
#'''