

class ColorScheme():
    '''
    Functions take a value between 0 and 1 and return
    an RGB tuple    
    '''
    def rainbow(self,value): 
        x = 1/7
        
        if value > x*6:
            
            v = (value-x*6)/x
            red = 255
            green = int(255*(v))
            blue = int(255*(v))
        
        elif value > x*5:
            v = (value-x*5)/x
            red = 255
            green = int(255*(1-v))
            blue = 0
        
        elif value > x*4:
            v = (value-x*4)/x
            red = int(255*(v))
            green = 255
            blue = 0
        
        elif value > x*3:
            v = (value-x*3)/x
            red = 0
            green = 255
            blue = int(255*(1-v))
        
        elif value > x*2:
            v = (value-x*2)/x
            red = 0
            green = int(255*(v))
            blue = 255
        
        elif value > x:
            v = (value-x)/x
            red = int(255*(1-v))
            green = 0
            blue = 255
            
        else:
            v = (value)/x
            red = int(255*(v))
            green = 0
            blue = int(255*v)
        
        return red,green,blue

    def rainbowtoomuchgreen(self,value): 
        
        if value > .8:
            v = (value-.8)/.2
            red = 255
            green = int(255*(1-v))
            blue = 0
        
        elif value > .6:
            v = (value-.6)/.2
            red = int(255*(v))
            green = 255
            blue = 0
        
        elif value > .4:
            v = (value-.4)/.2
            red = 0
            green = 255
            blue = int(255*(1-v))
        
        elif value > .2:
            v = (value-.2)/.2
            red = 0
            green = int(255*(v))
            blue = 255
        
        else:
            v = (value)/.22
            red = int(255*(1-v))
            green = 0
            blue = 255
        
        return red,green,blue

    def rainbow_old(self,value): 
        
        if value > .75:
            v = (value-.75)/.25
            red = 255
            green = int(255*(1-v))
            blue = 0
        
        elif value > .5:
            v = (value-.5)/.25
            red = int(255*(v))
            green = 255
            blue = 0
        
        elif value > .25:
            v = (value-.25)/.25
            red = 0
            green = 255
            blue = int(255*(1-v))
        
        else:
            v = (value)/.25
            red = 0
            green = int(255*(v))
            blue = 255
        
        return red,green,blue
            
    def redblue(self,value): 
        red     = int(  255*value     )
        green   = int(  0 )
        blue    = int(  255*(1 - value)     )
        return red, green, blue
    
    def whiteblack(self,value):
        red     = int(  255*value     )
        green   = int(  255*value     )
        blue    = int(  255*value     )
        return red, green, blue
    
    def mystery(self,value):
        
        if value > .75:
            v = (value-.75)/.25
            red = int(255*v)
            green = int(255*(1-v))
            blue = 0
        
        elif value > .5:
            v = (value-.5)/.25
            red = int(255*(1-v))
            green = int(255*v)
            blue = 0
        
        elif value > .25:
            v = (value-.25)/.25
            red =0
            green = int(255*v)
            blue = int(255*(1-v))
        
        else:
            v = (value)/.25
            red=0
            green = int(255*(1-v))
            blue = int(255*v)
        
        return red,green,blue
        



