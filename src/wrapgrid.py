

class WrapGrid():
    
    
    
    def layersphere(self, gridofcells):
        #connect left and right, top connects across top (same for bottom)
        depth = len(gridofcells)
        height = len(gridofcells[0])
        width = len(gridofcells[0][0])
        for zval in range(depth):
            for yval in range(height):
                for xval in range(width):
                    gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][yval][(xval+1) % width ])
                    gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][yval][(xval-1) % width ])
                    
                    if yval == 0 or yval + 1 == height:
                        gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][(yval)][int(xval + width/2) % width])
                    #elif yval + 1 == len(gridofcells):
                    #    gridofcells[yval][xval].addneighbor(gridofcells[(yval)][-xval])
                    else:
                        gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][(yval+1) % height ][xval])
                        gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][(yval-1) % height ][xval])
                        
                    if zval < depth - 1:
                        gridofcells[zval][yval][xval].addneighbor(gridofcells[zval+1][yval][xval])
                    if zval > 0:
                        gridofcells[zval][yval][xval].addneighbor(gridofcells[zval-1][yval][xval])
                        
            
        return gridofcells
    
    
    def flatsphere(self, gridofcells):
        #connect left and right, top connects across top (same for bottom)
        depth = len(gridofcells)
        height = len(gridofcells[0])
        width = len(gridofcells[1])
        for zval in range(depth):
            for yval in range(height):
                for xval in range(width):
                    gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][yval][(xval+1) % width ])
                    gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][yval][(xval-1) % width ])
                    
                    if yval == 0 or yval + 1 == height:
                        gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][(yval)][int(xval + width/2) % width])
                    #elif yval + 1 == len(gridofcells):
                    #    gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][(yval)][-xval])
                    else:
                        gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][(yval+1) % height ][xval])
                        gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][(yval-1) % height ][xval])
            
            return gridofcells
            
                        
    def torus(self, gridofcells):
        #connect left and right, connect top and bottom.
        depth = len(gridofcells)
        height = len(gridofcells[0])
        width = len(gridofcells[1])
        for zval in range(depth):
            for yval in range(height):
                for xval in range(width):
                    gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][(yval+1) % height ][xval])
                    gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][(yval-1) % height ][xval])
                    gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][yval][(xval+1) % width ])
                    gridofcells[zval][yval][xval].addneighbor(gridofcells[zval][yval][(xval-1) % width ])
            
            return gridofcells
        