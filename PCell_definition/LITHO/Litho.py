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
        #dbu definition is only for backwards compatibility with not "D" functions


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
            centered : bool = True          #True: Center tick is 0, False: counts from side
            markSize : float = 50.0         #Magnification of sign
            markStp : int = 1               #Increment number per long tick
            markTickSep : float = 5.0       #Separation between tick and marker 

        
        class HolowSq(pya.DPolygon):
            """
            A class is child of pya -> DPolygon
            Builds a hollow square from 2 parameters
            ...

            Attributes
            ----------
            side : float
                first name of the person
            wall : float
                family name of the person

            Methods
            -------
            N/A
            """
            def __init__(self, side, wall):

                self.a = side/2.0
                self.h = side/2.0-wall

                self.assign(pya.DPolygon(pya.DBox(-self.a, -self.a,self.a,self.a)))
                self.insert_hole(pya.DBox(-self.h, -self.h,self.h,self.h))

        '''
        Constants and variables:
            DIST_VERNIER : float  - distance of vernier structures center from center of square
            DBU : float - database unit for backwards compatibility

        '''
        DIST_VERNIER = 200
        DBU = 0.001

        sqFM = HolowSq(200.0, 20.0)
        sqOL = HolowSq(100.0, 20.0)

        verniL = Vernier(
                        tLong = 40.0,tShort = 30.0,
                        tWidth = 5.0,sp = 13.0,
                        tCnt = 12,group = 13
                        )
        verniC_OL = Vernier(
                        sp = 13.25, asc = False,
                        markers = True
                        )
        verniF_OL = Vernier(
                        tWidth = 5.0,sp = 15.1,
                        tCnt = 10,group = 5
                        )


        #First the squares
    

        #Verniers
        # it should be written in a way, that the vernier code could be reused later on somewhere else
        # or at least esilly rewritten 

        #Course vernier
        # it would be a cell, containing the FM and OL markers as like as the numbers given by standard
        # generator. 


        #Generate vernier array into the cell (layers would be taken from original parameters)
        def vernier_single_gen(param, t = pya.DCplxTrans(0,0)):
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
                t_loc = pya.DCplxTrans(loc * param.sp, param.offset)
                print(loc)
                if loc % param.group == 0: 
                    #possition of long tick
                    tick_t = tick_ln.transformed(t_loc)
                    verni_polys.append(tick_t.transformed(t))
                    
                    if param.markers:
                        print("Mark {:+.0f}".format(loc / param.group * param.markStp))
                        #gen = pya.TextGenerator.default_generator()
                        #text = gen.text("{:+.0f}".format(loc / param.group * param.markStp), 
                        #                DBU, param.markSize)
                        #text_t = text.transformed(t_loc)
                        #verni_polys.append(text_t.transformed(t))
                        
                        #TODO: generate marker labels
                else:
                    #position of short tick
                    tick_t = tick_sh.transformed(t_loc)
                    verni_polys.append(tick_t.transformed(t))

            return verni_polys
            

        #Square in square structure
        self.cell.shapes(self.l_layer).insert(sqFM)
        self.cell.shapes(self.lo_layer).insert(sqOL)

        verniers_poly = [[],[]]

        #Lay step first first:
        rot_matrix = [
                        [0,-1],
                        [1,0],
                        [0,1],
                        [-1,0]
        ]
        
        for i in range(0,4):
            t=pya.DCplxTrans(1.0, 90*i, False, 
                            rot_matrix[i][0] * DIST_VERNIER,
                            rot_matrix[i][1] * DIST_VERNIER)
            verniers_poly[0].append(vernier_single_gen(verniL, t))

        for i in [0,3]:
            t=pya.DCplxTrans(1.0, 180+90*i, False, 
                            rot_matrix[i][0] * DIST_VERNIER,
                            rot_matrix[i][1] * DIST_VERNIER)
            verniers_poly[1].append(vernier_single_gen(verniC_OL, t))

        for i in [1,2]:
            t=pya.DCplxTrans(1.0, 180+90*i, False, 
                            rot_matrix[i][0] * DIST_VERNIER,
                            rot_matrix[i][1] * DIST_VERNIER)
            verniers_poly[1].append(vernier_single_gen(verniF_OL, t))


        for item in verniers_poly[0]:
            for tick in item:
                self.cell.shapes(self.l_layer).insert(tick)

        for item in verniers_poly[1]:
            for tick in item:
                self.cell.shapes(self.lo_layer).insert(tick)

#STANDALLONE Testing
if TESTING:
    class LithoTesting(pya.Library):

        def __init__(self):

            self.description = "LithoTesting"

            self.layout().register_pcell("MA8_AutoMarkSqSq", MA8_AutoMarkSqSq())

            self.register("LithoTesting")

    LithoTesting()           