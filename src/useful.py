
import math,os,time


def zeropad(maxvalue=100,minimum = 0,extra=0):
    digits = math.floor(math.log10(maxvalue) + 1 + extra)
    if digits < minimum:
        digits = minimum 
    ftext = "{:0"+str(digits)+"d}"
    return ftext


def zeropad_test():
    f =  zeropad(130,1)
    for y in range(130):
        print(f.format(y))
        

def makefolder(newfolder = "img", startpath = "../media"):
    mediafolder = os.path.abspath(startpath)
    newdir = os.path.join(mediafolder,newfolder)
    #print(os.path.exists(newdir))
    if not os.path.exists(newdir):
        os.mkdir(newdir)
    #print(os.path.exists(newdir))
    return newdir

def uniquedirname(basename = "map"):
    datetime = time.strftime("%Y%m%d %H%M%S")     
    name = basename + " " + datetime
    return name

def dotprod(vector1,vector2):
    return sum(a*b for a,b in zip(vector1,vector2))

#makefolder(uniquedirname())

if __name__ == "__main__":    
    a = [i for i in range(10)]
    b = [-i for i in range(10)]
    
    c = [a[i]*b[i] for i in range(10)]
    print(c)
    print(sum(c))
    
    x = sum(t*n for t,n in zip(a,b))
    print(x)
    print(dotprod(a,b))
    d= a*3
    print(d)
