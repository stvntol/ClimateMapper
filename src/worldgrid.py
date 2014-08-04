

from weathernode import WeatherNode
from wrapgrid import WrapGrid
import math
from useful import zeropad as zp

class WorldGrid(WrapGrid):
        
    def __init__(self, width = 22, height = 11, depth = 1, radius = 6000, baseEnergy = 300, shape = "layersphere"):
        
        #Dimensions
        self.shape = shape
        self.height = height
        self.width = width
        self.depth = depth
        self.area = height*width
        
        self.radius = radius
        self.altitude = 11
        #List of average values of grid
        #at the moment there is only one subgrid type. If needed this should become a dictionary

        self.subgrids = []
        self.averages_grid = []
        self.averages_row =[]
        
        #Create a grid of WeatherNodes
        self.grid = self.createworldgrid(baseEnergy)
        
        self.grid_Tmp = self.createsubgrid("Tmp")
        self.grid_P = self.createsubgrid("P")
        self.grid_Nk = self.createsubgrid("Nk")
        self.grid_volume = self.createsubgrid("volume")
        
        self.grid_Tmp_side = self.createsideview("Tmp")
        self.grid_P_side = self.createsideview("P")
        self.grid_Nk_side = self.createsideview("Nk")
        
        self.thermogrids= {"Tmp":[self.grid_Tmp],
                           "P":[self.grid_P],
                           "Nk":[self.grid_Nk],
                           "volume":[self.grid_volume],
                           
                           #"Tmp_rows":[],
                           #"P_rows":[],
                           #"Nk_rows":[],
                           #"V_rows":[],
                           
                           #"Tmp_avg":[],
                           #"P_avg":[],
                           #"Nk_avg":[],
                           #"V_avg":[]
                           }
        
        
        self.assignneighbors(shape)
        
        self.records_uptodate = True
        
        #self.recordkeeping()
        #Heating and Cooling Rate
        #self.hRate = .05
        #self.cRate = self.hRate*sum([math.sin(math.pi/(self.height-1)*y) for y in range(self.height)])/self.height
        
        #self.hRate = 1000*(4.5*10**8/self.area)/((60*60*24)/2)/4 #1: Sun W/m, 2: area, convert to half day, heat capacity of water
        #self.cRate = 6*(10**-8)*.38/(60*60*24) #*(4.5*10**14/self.area) # 1: botzmann constant, 2: area, 3: .38 is emissivity of soil, 4 convert to days
        
        #self.hRate = 1000*(4.5*10**5/self.area)/((60*60*24)/2)/4
        #self.cRate = 6*(10**-8)*.38/(60*60*24)
        
        #self.hRate = 1000*(4.5*10**6/self.area)/((60*60*24)/2)/4
        #self.cRate = self.hRate/300**4
        #self.baseT = .5*self.hRate/4
        
        self.hRate = .001364 # 2/3*.7*1367 W/m^2 in J/hour/km^2
        self.cRate = 1.388016*10**-13 #.612*4*5.67×10^-8
        self.baseT = 0#*.5*self.hRate/4
        
        
        
    """ Grid Creation"""
                    
    def createworldgrid(self, baseEnergy):
        #creates grid of WeatherNodes
        volconst = 2*math.pi*self.altitude*self.radius**2/(self.height*self.width*self.depth)
        
        grid =[]
        for c in range(self.depth):
            Z = []
            if c > 0:
                matter = "air"
            else:
                matter = "water"
            for b in range(self.height):
                Y = []
                vol = volconst*(math.cos(math.pi/self.height * b) - math.cos(math.pi/self.height *(b + 1)))
                for a in range(self.width):
                    Y.append(WeatherNode(Tmpvalue= baseEnergy - 100 +(100*math.sin(math.pi/(self.height-1)*b)), x = a, y = b, z=c, volume = vol, material = matter,  maxaltitude = self.altitude, altitudedivisions = self.depth))
                    #Y.append(WeatherNode(Tmpvalue= 250, x = a, y = b, z=c, volume = vol, material = matter))
                    
                Z.append(Y)
            grid.append(Z)

        return grid
    
    def createsubgrid(self, selectedvalue, elevation = 0):
        #creates a grid of specified property of each node 
        #Needed to construct images /produce useful printout
        if elevation >= self.depth:
            elevation =self.depth - 1
        Q = "n." + selectedvalue
        subgrid = [[ eval(Q) for n in row] for row in self.grid[elevation]]  # @UnusedVariable Used in eval()
        
        return subgrid
    
    def createsideview(self, selectedvalue):
        #creates a grid of specified property of each node 
        subgrid = []
        q = "self.grid[z][y][x]." + selectedvalue

        x = int(self.width/2)
        for y in range(self.height):
            yz = []
            for z in range(self.depth):
                a = eval(q)
                yz.append(a)
            subgrid.append(yz)
            
        return subgrid
    
    


    """Actions on the Grid"""
    def assignneighbors(self, shape = "layersphere"):
        
        try:
            f = "self." + shape
            wrap = eval(f)
            self.grid= wrap(self.grid)
        
        except Exception as e: 
            print(e)
            wrap = self.layersphere
            self.grid= wrap(self.grid)
        
    def cool(self):
        #for layer in self.grid:
            layer = self.grid[-1]
            for row in layer:
                for cell in row:
                    #cell.Tmp_received -= ((cell.z + 1)/self.depth)*self.cRate*cell.Tmp**4           
                    cell.Tmp_received -= self.cRate*cell.Tmp**4           
        
    def warm(self, tilt = 0):
        for altitude in range(self.depth):
            if altitude == 0:
                base = self.baseT
            else:
                base = 0
                
            for latitude in range(self.height):
                #gain = self.hRate*math.sin(math.pi/(self.height)*(latitude+.5) + tilt) + base
                gain = self.hRate*math.sin(math.pi/(self.height)*(latitude+.5) + tilt) + base
                
                for node in self.grid[altitude][latitude]:
                    node.Tmp_received += gain #*(node.volume/node.altitudeconstant)/node.Nk
#        for row in self.grid:
#            latitude = row[0].y
#            gain = rate*math.sin(math.pi/(self.height-1)*latitude + tilt)
#            for cell in row:
#                cell.received += gain
                
    def update(self, keeprecords = False):
        #Runs every node's update function from upper left to lower right
        for layer in self.grid:
            for row in layer:
                for node in row:
                    node.update()
        #update subgrid for images
        
        self.grid_Tmp = self.createsubgrid("Tmp")
        self.grid_P = self.createsubgrid("P")
        self.grid_Nk = self.createsubgrid("Nk")
        
        self.grid_Tmp_side = self.createsideview("Tmp")
        self.grid_P_side = self.createsideview("P")
        self.grid_Nk_side = self.createsideview("Nk")
        
        if keeprecords == False:        
            self.records_uptodate = False
        else:
            self.recordstate()
                
    def updateREV(self):
        #Runs every node's update function from lower right to upper left
        for y in range(self.height):
            for x in range(self.width):
                self.grid[self.height-y-1][self.width-x-1].update()
    
    
    def updateFull(self,keeprecords = False):
        # Nodes update in two phase a calculation phase and a give/receive phase
        # Separate phases prevents energy transfer calculations running asymmetrically
        # i.e. Heating faster in the direction of updates
        self.update()
        self.update(keeprecords)
    
    
    """************************************************************************************************""" 
    """Gather information on grids""" 
    def recordstate(self):
        thermoproperties = ["Tmp","P","Nk"]
        for aspect in thermoproperties:
            grid_torecord = eval("self.grid_"+aspect)
            self.thermogrids[aspect].append(grid_torecord)
            
        self.records_uptodate = True
    
    """Print information on grids""" 
    def printaspectsummary(self, aspect= "Tmp"):
        print(aspect+":")
        initial = sum([sum(row) for row in self.thermogrids[aspect][0]])
        final = sum([sum(row) for row in eval("self.grid_"+ aspect)])
        print("Initial:\t{:>f}".format(initial), initial/self.area, sep="\t")
        print("Final:\t\t{:>f}".format(final), final/self.area,sep="\t")
        print("Difference:\t{:>f}".format(final-initial),(final-initial)/self.area,sep="\t", end="\t")
        print("{:%}".format((final-initial)/initial))

    def printrowaverages(self, usegrid = -1 , aspect = "Tmp"):
        if usegrid == -1:
            grid = eval("self.grid_"+aspect)
        else:
            grid = self.thermogrids[aspect][usegrid]
            
        print(usegrid, end = " ")
        for row in grid:
            print( sum(row)/len(row), end = " ")
            #print(sum(row)/len(row))
        print()
    
    def printrowsums(self, usegrid = -1 , aspect = "Tmp", output = True):
        if usegrid == -1:
            grid = eval("self.grid_"+aspect)
        else:
            grid = self.thermogrids[aspect][usegrid]
        if output:    
            print(usegrid, end = " ")
        total = 0
        for row in grid:
            s = sum(row)
            total += s
            if output:
                print( s, end = " ")
            #print(sum(row)/len(row))
        if output:
            print("Total: ", total)
        return total
    

    """************************************************************************************************""" 
    
    def printsummary(self):
        initial = sum([sum(row) for row in self.subgrids[0]])
        final = sum([sum(row) for row in self.grid_Tmp])
        print("Initial:\t{:>f}".format(initial), initial/self.area, sep="\t")
        print("Final:\t\t{:>f}".format(final), final/self.area,sep="\t")
        print("Difference:\t{:>f}".format(final-initial),(final-initial)/self.area,sep="\t", end="\t")
        print("{:%}".format((final-initial)/initial))

    
    def recordkeeping(self):
        #update list of subgrids and list of average values
        self.subgrids.append(self.grid_Tmp)
        
        row_averages = self.take_row_averages(self.grid_Tmp)
        
        self.averages_row.append(row_averages)
        self.averages_grid.append(sum(row_averages)/len(row_averages))
        
        self.records_uptodate = True
    
    def take_row_averages(self,grid):
        row_averages = []
        for row in grid:
            average = sum(row)/len(row)
            row_averages.append(average)
        return row_averages
    
    def take_grid_average(self,grid):
        average = sum([sum([n.Tmp for n in row]) for row in self.grid[0]])/self.area
        return average

    """Retrieve Information from grids"""
    def printlatestgrid(self):
            self.printsubgrid(self.grid_Tmp)
    
    def printrecords_latest(self):
        if self.records_uptodate == False:
            self.recordkeeping()
        i = len(self.subgrids) -1
        print(i," Average Value: ",self.averages_grid[i])
        
        for r in range(self.height):
            print(zp(self.height).format(r),self.averages_row[i][r], [str(n)[0:5] for n in self.subgrids[i][r]], sep= ": ")
        print()
    
    def printrecords_all(self):
        for i in range(len(self.subgrids)):
            print(i," Average Value: ",self.averages_grid[i])
            self.printsubgrid(self.subgrids[i])
            
    def printsubgrid(self, grid ):
            for row in grid:
                print( [str(n)[0:5] for n in row])
            print()
    




    
