import pya
import math
import numpy

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
    

    


    #def display_text_impl(self):
        # Provide a descriptive text for the cell
    #return "AMR_Disk(D={:.3f}, AsyV={}".format(self.dia, self.asy_vector)

  def coerce_parameters_impl(self):
    # TODO: use x to access parameter x and set_x to modify it's value
    rs = None
  def produce_impl(self):
    #Using Double values only - no dbu required (alternatively use scaling instead)

    #Internal constants

    class HolowSq(side, wall):
        def __init__(self, side, wall):
            self.a = side
            self.w = wall
        def 


    FMSq = {
        "a" : 200.0,    #Side lenght of the center square FM
        "wall": 20.0    #Wallthickness of the center square FM
    }
    OLSq = {
        "a" : 100.0,    #Side lenght of the center square OL
        "wall": 20.0    #Wallthickness of the center square OL
    }
    VerniC = {
        "long" : 50.0,  #Long tick lenght
        "short": 30.0,  #Short tick lenght
        "wall": 5.0,    #Tick wall thickness
        "spL" : 8.0,    #Spacing first exposure
        "spOL" : 8.5,   #Spacing overlay exposure
        "cnt" : 12      #Number of ticks overall
    }
    VerniF = {
        "long" : 50.0,  #Long tick lenght
        "short": 30.0,  #Short tick lenght
        "wall": 5.0,    #Tick wall thickness
        "spL" : 10.0,    #Spacing first exposure
        "spOL" : 10.1,   #Spacing overlay exposure
        "cnt" : 10      #Number of ticks overall
    }
    
    #First the squares
    FMSq = pya.DBox(FMSq.a)