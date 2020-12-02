import pya
# import math
# import numpy
from dataclasses import dataclass

TESTING = True


class MA8_AutoMarkSqSq(pya.PCellDeclarationHelper):

    def __init__(self):

        # Important: initialize the super class
        super(MA8_AutoMarkSqSq, self).__init__()

        # declare the parameters
        #LayerParameters
        self.param("l", self.TypeLayer, "First Marker layer", 
                    default = pya.LayerInfo(1, 0, "MarkerFM"))

        self.param("FMTone", self.TypeBoolean, "First Marker Tone", 
                    choices = [["Possitive", False],["Negative", True]],
                    default= True)

        self.param("lo", self.TypeLayer, "Overlay Marker layer", 
                    default = pya.LayerInfo(2, 0, "MarkerOL"))
        self.param("OLTone", self.TypeBoolean, "Overlay Marker Tone", 
                    choices = [["Possitive", False],["Negative", True]], default= True)

        self.param("StepName", self.TypeString, "Name of Step (e.g. 2A)", default = "2A") 
        
        #debuging
        self.param("debug", self.TypeBoolean, "Debug output", 
                    choices = [["No", False],["Yes", True]], default= True) 
    

    

    def display_text_impl(self):
    # Provide a descriptive text for the cell
        return "MA8_AutoMarkSqSq_"+self.StepName

    def coerce_parameters_impl(self):
        # TODO: use x to access parameter x and set_x to modify it's value
        rs = None
    def produce_impl(self):
    #Using Double values only - no dbu required (alternatively use scaling instead)

        @dataclass
        class SqinSq:
            a : float       = 100.0         #Side lenght of the center square
            wall : float    = 10.0          #Wallthickness of the center square FM

        @dataclass
        class Vernier:
            tLong  : float = 50.0           #Long tick lenght
            tShort : float = 30.0           #Short tick lenght
            tWidth : float = 5.0            #Tick wall width
            sp : float    = 8.0             #Spacing first exposure
            offset : float = 0.0            #offset in y direction              
            tCnt : int     = 12             #Number of ticks per side (not inc. center)
            group : int    = 4              #Number of ticks per group (resolution)
            markers : bool = False          #Allow markers above / bellow ticks 
            asc : bool = False              #ascending of Label signs (+++/---)
            tLabelInv : bool = False        #Inversion of Label signs (+++/---)
            centered : bool = True          #True: Center tick is 0, False: counts from side
            markSize : float = 10.0         #Magnification of sign
            markStp : int = 1               #Increment number per long tick
            markTickSep : float = 5.0       #Separation between tick and marker 
        


        sqFM = SqinSq(200.0, 20.0)
        sqOL = SqinSq(100.0, 20.0)


        #TODO: redo parameters
        verniC_L = Vernier()
        # verniF_R = Vernier(50.0, 30.0, 5.0, 10.0, 10.1, 10)
        # verniC_B = VerniC_L
        # verniF_T = VerniF_R
        # verniC_B.tLabelInv = True
        # verniF_T.tLabelInv = True

        #First the squares
    

        #Verniers
        # it should be written in a way, that the vernier code could be reused later on somewhere else
        # or at least esilly rewritten 

        #Course vernier
        # it would be a cell, containing the FM and OL markers as like as the numbers given by standard
        # generator. 


        #Generate vernier array into the cell (layers would be taken from original parameters)
        def vernier_single_gen(param):
            """
            Returns list of polygons of vernier generated. Optionally with describtors
            
            Cleaner and more universal in comparism to previous pya.Cell atempt
                it doesn't require the layer and layout to be passed
            Parameters
            ----------
                param : obj
                    dataclass containing the vernier design parameters
                    class Vernier:
                        tLong  : float = 50.0           #Long tick lenght
                        tShort : float = 30.0           #Short tick lenght
                        tWidth : float = 5.0            #Tick wall width
                        sp : float    = 8.0             #Tick Spacing
                        tCnt : int     = 12             #Number of ticks overall
                        group : int    = 4              #Number of ticks per group (resolution)
                        markers : bool = False          #Allow markers above / bellow ticks 
                        asc : bool = False              #ascending of Label signs (+++/---)
                        centered : bool = True          #True: Center tick is 0, False: counts from side
                        markSize : float = 10.0         #Magnification of sign
                        markStp : int = 1               #Increment per tick
                        markTickSep : float = 5.0       #Separation between tick and marker 
            """
            tick_ln = pya.DBox(
                        -param.tWidth/2,
                        0.0,
                        param.tWidth/2,
                        param.tLong)

            tick_sh = pya.DBox(
                        -param.tWidth/2,
                        0.0,
                        param.tWidth/2,
                        param.tShort)

            #verniCell = pya.Cell()
            verni_polys = []

            #get the generator direction 
            if param.centered:
                if param.asc:
                    tick_range = range(-param.tCnt, param.tCnt+1, 1)
                else:
                    tick_range = range(param.tCnt, -param.tCnt-1, -1)
            else:
                if param.asc:
                    tick_range = range(-param.tCnt, 1, 1)
                else:
                    tick_range = range(param.tCnt, -1, -1)

            for loc in tick_range:
                t_loc = pya.DTrans(loc * param.sp, param.offset)
                if loc % param.group == 0: 
                    #possition of long tick
                    verni_polys.append(tick_ln.transformed(t_loc))
                    #verniCell.shapes(layer).insert(tick_ln.transformed(t_loc))
                    if param.markers:
                        pass
                        #TODO: generate marker labels
                else:
                    #position of short tick
                    verni_polys.append(tick_sh.transformed(t_loc))

            return verni_polys

        
        VerniTest = vernier_single_gen(verniC_L)
        t=pya.DCplxTrans(1.0, 0, False, 150, 150)
        for tick in VerniTest:
            self.cell.shapes(self.l_layer).insert(tick.transformed(t))

#STANDALLONE Testing
if TESTING:
    class LithoTesting(pya.Library):

        def __init__(self):

            self.description = "LithoTesting"

            self.layout().register_pcell("MA8_AutoMarkSqSq", MA8_AutoMarkSqSq())

            self.register("LithoTesting")

    LithoTesting()           