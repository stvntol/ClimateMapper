
#import colorgrid, windowimage, math
from useful import dotprod
import math

class NodeMatter():
    
    def air(self):
        self.density = 1.225 #kg/m^3
        self.viscosity = 1.48 #micro m^2/s

class WeatherNode(NodeMatter):

    
    def __init__(self, Tmpvalue = 300, x=0, y=0, z=0, material = "water", volume = 1080000000, particles = 1250, maxaltitude = 12, altitudedivisions = 3 ):
        
        self.x = x
        self.y = y
        self.z = z
        
        self.air()
        
        self.Tmp = Tmpvalue # Temperature
        self.Tmp_new = self.Tmp
        self.Tmp_received = 0
        self.Tmp_given = [self.Tmp]
        
        self.P = 101*math.exp(-34.1814052*(z*maxaltitude/altitudedivisions)/self.Tmp)
        self.P_new = self.P
        self.P_received = 0
        
        
        self.Nk = int(round(self.P*volume/self.Tmp))#particles #Number of Particles
        self.Nk_new = self.Nk
        self.Nk_received = 0
        self.Nk_given = [self.Nk]

        self.volume = volume
        
       
        self.particlemass = 893
        # mass of atmosphere*3/4 (in region of concern)/approximate volume in xyz units
        # divided by initial number of particles (1250) times boltzmann constant
        
        self.material = material
        self.altitudeconstant = maxaltitude/altitudedivisions #*self.particlemass 0*63504*63504=127008/2 = g/2 in km/hr^2 
        
        '''
        self.air_x = 0
        self.air_y = 0
        self.air_z = 0
        '''
        
        self.neighbors = []
        
        self.giving = True
        
        self.check = 2
        self.finddensity()
        
    def finddensity(self):
        self.density = 0.028964 * self.P/(8.314*self.Tmp)
        self.masspressure = self.density*self.altitudeconstant*1000*9.8
         
        # molar mass * pressure / (ideal gas constant * temperature)
        
    def addneighbor(self,N):
        self.neighbors.append(N)
    
    def convection(self):
        nP = [self.P]
        #nTmp = [self.Tmp]
        #nNk= [self.Nk]
        #nVol = [self.volume]
        #nz = [self.z]
        nindex =[]
        P_diff = 0
        for node in self.neighbors:
            if self.P > node.P  and node.z == self.z:
                nP.append(node.P)
                #nTmp.append(node.Tmp)
                #nNk.append(node.Nk)
                #nz.append(node.z) 
                #nVol.append(node.volume)
                nindex.append(self.neighbors.index(node))
                P_diff += self.P-node.P
                
            elif  self.z > node.z and self.P + self.masspressure > node.P:
                # If I'm above you and you can't support me I pass to you
                nP.append(node.P - self.masspressure )
                nindex.append(self.neighbors.index(node))
                P_diff += self.P-node.P - self.masspressure
                
            elif  self.z < node.z and self.P > node.P + node.masspressure :
                # If I'm bellow you and you can't suppress me I pass to you
                nP.append(node.P + node.masspressure )
                nindex.append(self.neighbors.index(node))
                P_diff += self.P-node.P + node.masspressure
                
                
        if len(nindex) >0:
            avgP = sum(nP)/len(nP)
            Nk_diff = int(round(-self.Nk* (avgP/self.P-1)/1)) #the denominator is the number of updates before the values would reach their average 
            #self.Nk_new = self.Nk - Nk_diff
            self.Nk_new -=Nk_diff
            
            #giveaway = 0
            for index in nindex:
                given = int(round(Nk_diff*(self.P-self.neighbors[index].P)/P_diff))
                self.neighbors[index].Nk_given.append(given )
                self.neighbors[index].Tmp_given.append(self.Tmp) # - 6.5*self.altitudeconstant*(self.neighbors[index].z-self.z))
                #giveaway += given
            '''
            if giveaway != Nk_diff:
                print("DID NOT ADD")
                print("(x,y,z):",self.x,self.y,self.z, sep =" ")
            else:
                print("works",self.Nk, self.Nk_new, sep =" ")
            '''
                
    def updatethermo(self):
        #print(self.x, self.y, self.Nk_given,self.Nk_new)
        self.Nk_given[0] = self.Nk_new
        self.Nk = sum(self.Nk_given)
        self.Nk_new = self.Nk
        self.Tmp = dotprod(self.Tmp_given,self.Nk_given)/self.Nk + self.Tmp_received
        self.P = self.Nk*self.Tmp/self.volume
        
        self.Tmp_received = 0
        
        self.Nk_given = [self.Nk]
        self.Tmp_given = [self.Tmp]
        self.finddensity()

        
    def update(self):
        if self.giving == True:
            self.convection()
            #self.give()
            #self.distribute()
            self.giving = False
        else:
            self.updatethermo()
            #self.gain
            self.giving = True
            
'''            
    def distribute(self):
        
        nP = [self.P]
        nTmp = [self.Tmp]
        nNk= [self.Nk]
        nVol = [self.volume]
        nz = [self.z]
        nindex =[]
        for node in self.neighbors:
            if node.P < self.P:
                nP.append(node.P)
                nTmp.append(node.Tmp)
                nNk.append(node.Nk)
                nz.append(node.z) 
                nVol.append(node.volume)
                nindex.append(self.neighbors.index(node))
        #if len(nTmp) + len(nNk) + len(nVol) +len(nz) == 4*len(nP):
        #    lessers = len(nP)
        #Uconst = sum([[nTmp[i]*nNk[i] for i in range(lessers)]])
        #Uconst = dotprod(nTmp,nNk) + (2/3)*self.gravconstant*(dotprod(nz,nNk)+sum(nNk))*(1-1/len(nP))
        Uconst = dotprod(nTmp,nNk)
        self.Tmp_new = Uconst/sum(nNk)
        self.P_new = Uconst/sum(nVol)
        self.Nk_new = sum(nNk)/sum(nVol)*self.volume
        for index in nindex:
            self.neighbors[index].Tmp_received = (self.Tmp_new - 2/3*(self.neighbors[index].z-self.z)/(sum(nNk)/sum(nVol)*self.neighbors[index].volume))- self.neighbors[index].Tmp 
            self.neighbors[index].P_received = self.P_new - self.neighbors[index].P
            self.neighbors[index].Nk_received = sum(nNk)/sum(nVol)*self.neighbors[index].volume - self.neighbors[index].Nk
    
    
    def findNk(self):
        newNk = self.P/self.Tmp*self.volume
        self.Nk_received = newNk -self.Nk
        self.Nk_new = newNk
    
                
    def give(self):
        nTmp = [n.Tmp for n in self.neighbors]
        smaller_index = []
        smaller_value = []
        for i in range(len(nTmp)):
            if nTmp[i] < self.Tmp:
                smaller_index.append(i)
                smaller_value.append(nTmp[i])
                
        meanTmp = sum(smaller_value,self.Tmp)/(len(smaller_value)+1)
        self.Tmp_new = meanTmp
        transfer_values = []
        for value in smaller_value:
            transfer_values.append(meanTmp-value)
        
        for i in range(len(transfer_values)):
            self.neighbors[smaller_index[i]].Tmp_received += transfer_values[i] 
    
    def gain(self):
        self.Tmp = self.Tmp_new + self.Tmp_received
        self.Tmp_received = 0
        self.P = self.P_new + self.P_received
        self.P_received = 0
        self.Nk = self.Nk_new + self.Nk_received
        self.Nk_received = 0
        #This may be over constrained, in which case change it so particles are received and new pressure is calculated
        if self.P != self.Nk*self.Tmp/self.volume and self.check > 102 and self.check < 102:
            print("P is off by: {:.2%} in node".format(  (self.P - self.Nk*self.Tmp/self.volume)/(self.Nk*self.Tmp/self.volume))
                  ,self.x,self.y,self.z, sep=" ")
            self.check -= 1
        else:
            self.check += 1
'''