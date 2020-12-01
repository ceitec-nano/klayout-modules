import pya
import math
import numpy
from dataclasses import dataclass


class MA8_AutoMarkSqSq(pya.PCellDeclarationHelper):

    def __init__(self):

    # Important: initialize the super class
    super(MA8_AutoMarkSqSq, self).__init__()

    # declare the parameters
    #LayerParameters
    self.param("l", self.TypeLayer, "First Marker layer", default = pya.LayerInfo(1, 0, "MarkerFM"))
    self.param("FMTone", self.TypeBoolean, "First Marker Tone", choices = [["Possitive", False],["Negative", True]], default= True)

    self.param("lo", self.TypeLayer, "Overlay Marker layer", default = pya.LayerInfo(2, 0, "MarkerOL"))
    self.param("OLTone", self.TypeBoolean, "Overlay Marker Tone", choices = [["Possitive", False],["Negative", True]], default= True)

    self.param("StepName", self.TypeString, "Name of Step (e.g. 2A)", default = "2A") 
    
    #debuging
    self.param("debug", self.TypeBoolean, "Debug output", choices = [["No", False],["Yes", True]], default= True) 
    

    

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
            spL : float    = 8.0            #Spacing first exposure
            spOL : float   = 8.5            #Spacing overlay exposure
            tCnt : int     = 12             #Number of ticks overall
            group : int    = 4              #Number of ticks per group (resolution)
            tsep : float   = 5.0            #Separation between tick arrays
            tLabelInv : bool = False        #Inversion of Label signs (+++/---)

        sqFM = SqinSq(200.0, 20.0)
        sqOL = SqinSq(100.0, 20.0)
        verniC_L = Vernier(50.0, 30.0, 5.0, 8.0, 8.5, 12)
        verniF_R = Vernier(50.0, 30.0, 5.0, 10.0, 10.1, 10)
        verniC_B = VerniC_L
        verniF_T = VerniF_R
        verniC_B.tLabelInv = True
        verniF_T.tLabelInv = True

        #First the squares
    

        #Verniers
        # it should be written in a way, that the vernier code could be reused later on somewhere else
        # or at least esilly rewritten 

        #Course vernier
        # it would be a cell, containing the FM and OL markers as like as the numbers given by standard
        # generator. 

        def vernier_gen(param, layer)