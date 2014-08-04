'''
Created on Mar 22, 2014

@author: Flocko
'''

from PIL import Image
from colorscheme import ColorScheme
import os
from useful import makefolder

class GridDraw(ColorScheme):
    
        
    def __init__(self, savedir = "C:\\Users\\Flocko\\workspace\\pyClim\\sandbox\\img", temprange=(200,325)):
        self.savedir = savedir
        self.scaledir = makefolder("scale",savedir)
        self.high = temprange[1]
        self.low = temprange[0]
        self.drawscale()
        
    def draw(self, grid, name="image"):
        pic = self.colorgrid(grid)
        self.savepicture(pic, name, self.savedir)
            
            
    def colorgrid(self,grid):
        #Create new image and return it
        picture = Image.new("RGB",(len(grid[0]),len(grid)))
        pixels = picture.load()
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                pixels[x,y]= self.assigncolor(grid[y][x])
        return picture
    
    def savepicture(self, picture, filename, location ="."):
        #save image
        savedir = os.path.join(location,filename)
        picture.save(savedir)
                
    def assigncolor(self, value=0):
        #assign an RGB value based on a given value
        
        value = (value - self.low) /(self.high - self.low)
        if value > 1:
            p = (255,255,255)
            value = 1
        elif value < 0:
            p = (0,0,0)
            value = 0
        else:
                
            p= self.rainbow(value) 
        return p
    
    def drawscale(self):
        scale = self.colorscale()
        self.savepicture(scale,"scale.png",self.scaledir)
        
    def colorscale(self):
        colorrange = self.high-self.low+3
        scale = Image.new("RGB",(colorrange,1))
        pixels = scale.load()
        
        for x in range(colorrange):
            pixels[x,0] = self.assigncolor(x+self.low-1)
        return scale      

    #print(assigncolor(.5))


'''
low = 200
high = 325

r = high -low + 3

print(r)

for i in range(r):
    x = i+ low -1
    print((x-low)/(high-low))
'''