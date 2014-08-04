
import guiwindow, colorgrid, math
import worldgrid
from useful import zeropad as zp
from useful import makefolder, uniquedirname

settings = {
'height'    :41,
'width'     :82,
'depth'     :4,
'loops'     :20,
'basename'  :"Temp test",
'pad'       :3,
'tilt'      :False,
#'temprange' :(500,6000), #Number of particles
'temprange' :(200,333), #Temperature
#'temprange' :(10,150), #Pressure


#'units'     :"C",
}

default = {
'height'    :41,
'width'     :82,
'depth'     :1,
'loops'     :300,
'basename'  :"map",
'pad'       :3,
'tilt'      :True,
'temprange' :(213,340),
'units'     :"K",
}



def main(s = default):
    
    for key in default:
        if key not in s:
            s[key] = default[key]
    
    #Create save directory
    longname = s['basename']+" "+ str(s['loops']) + "days"+" "+str(s['height']*2)+"x"+str(s['height']) 
    foldername = uniquedirname(longname)
    savefolder = makefolder(foldername)
    
    #create world
    world = worldgrid.WorldGrid(width = s['height']*2, height = s['height'], depth= s['depth'], baseEnergy=325, shape = "layersphere")
    
    #create image drawer
    drawer = colorgrid.GridDraw(savefolder, s['temprange'])
    
    #draw initial state
    picture_name = s['basename']+"x"+zp(s['loops'],s['pad']).format(0) +".png"
    drawer.draw(world.grid_Tmp, picture_name)
    #drawer.draw(world.grid_Nk_side, "Nk_"+picture_name)
    '''
    print()
    for z in range(s['depth']):
        print(world.grid[z][0][0].P)
        
    print("{:.2%}".format(0))
    '''
    
    for i in range(s['loops']):
        # 1 loop = 1 day
        
        if s['tilt'] == True:
            axialtilt = 23.5*math.pi*math.sin(2*math.pi/365* i)/180
        else:
            axialtilt = 0 
        
        #axialtilt = math.pi/2
        #axialtilt = 23.5*math.pi*math.sin(2*math.pi/365* i)/180
        #print("tilt", axialtilt)
        #world.cool(cRate)
        #world.warm(hRate, axialtilt)
        
        world.cool()
        world.warm(tilt = axialtilt)
        
        # 1 updateFull represents 4 hours for the Temperature to distribute
        '''
        a = world.printrowsums(i,"Nk",False)
        b = world.printrowsums(i,"Tmp",False)
        c = world.printrowsums(i,"P",False)
        '''
        for _ in range(3):
            world.updateFull()
        #print("1", end=" ")
        
        
        world.updateFull(True)
        
        #print("2", end=" ")
        '''
        a1 = world.printrowsums(i+1,"Nk", False)
        b1 = world.printrowsums(i+1,"Tmp", False)
        c1 = world.printrowsums(i+1,"P", False)
        '''
        picture_name = s['basename']+"x"+zp(s['loops'],s['pad']).format(i) +".png"
        drawer.draw(world.grid_Tmp, picture_name)
        #drawer.draw(world.grid_P, "P_"+picture_name)
        #drawer.draw(world.grid_Nk_side, "Nk_side"+picture_name)
        
        print("{:3.2%}".format((i+1)/s['loops']), end=" \t")
        
        #print("Nk : {:.4%} diff".format((a-a1)/a),"Tmp: {:.4%} diff".format((b-b1)/b),"Pr : {:.4%} diff".format((c-c1)/c), sep="\t" ) 
    #print the initial nad final lateral temperature distribution  
    print()
    
    #print("1", end=" ")
    #world.printrowsums(s['loops'],"Nk")
    
    
    aspect = ["Tmp", "P", "Nk"]
    for v in aspect:
        world.printaspectsummary(v)
        #for i in range(s['loops']+1):
        #    world.printrowsums(i,v)
    print()
    '''
    for y in range(s['height']):
        print(world.grid[0][y][0].volume)
    '''
        
    
    
    '''
    world.printaspectsummary("Tmp")
    world.printrowaverages(0,"Tmp")
    world.printrowaverages(-1,"Tmp")
    
    world.printaspectsummary("P")
    world.printrowaverages(0,"P")
    world.printrowaverages(-1,"P")
    
    world.printaspectsummary("Nk")
    world.printrowaverages(0,"Nk")
    world.printrowaverages(-1,"Nk")
    '''
    '''
    print("heating:", world.hRate)
    print("cooling:",world.cRate)
    print("BaseT:",world.baseT)
    '''
    guiwindow.show(savefolder, s['temprange'], s['units'])

if __name__ == "__main__":
    main(settings)
