'''
@author: Steven Toledo
'''
from main import main

settings = {
'height'    :41,
'width'     :82,
'depth'     :4,
'loops'     :10,
'basename'  :"Temp test",
'pad'       :3,
'tilt'      :False,
#'temprange' :(500,6000), #Number of particles
'temprange' :(200,333), #Temperature
#'temprange' :(10,150), #Pressure


#'units'     :"C",
}

if __name__ == "__main__":
    main(settings)
