import pya
import math, numpy

TESTING = True

class TestTraining(pya.PCellDeclarationHelper):

    def __init__(self):

        # Important: initialize the super class
        super(MA8_AutoMarkSqSq, self).__init__()

        # declare the parameters
        #LayerParameters
        self.param("l", self.TypeLayer, "First Marker layer", 
                    default = pya.LayerInfo(1, 0, "MarkerFM"))
        

        #debuging
        self.param("debug", self.TypeBoolean, "Debug output", 
                    choices = [["No", False],["Yes", True]], default= True) 
  
    def display_text_impl(self):
    # Provide a descriptive text for the cell


    def coerce_parameters_impl(self):
        # TODO: use x to access parameter x and set_x to modify it's value
        rs = None

    def produce_impl(self):
        
class Square(pya.PCellDeclarationHelper):

    def __init__(self):

        # Important: initialize the super class
        super(Square, self).__init__()

        # declare the parameters
        #LayerParameters
        self.param("l", self.TypeLayer, "First Marker layer", 
                    default = pya.LayerInfo(1, 0, "MarkerFM"))
        self.param("side_a", self.TypeDouble, "Size of Square", 
                    default = 10.0)
        

        #debuging
        self.param("debug", self.TypeBoolean, "Debug output", 
                    choices = [["No", False],["Yes", True]], default= True) 
  
    def display_text_impl(self):
    # Provide a descriptive text for the cell
        return "Square_{:.1f}um".format(self.side_a)


    def coerce_parameters_impl(self):
        # TODO: use x to access parameter x and set_x to modify it's value
        rs = None

    def produce_impl(self):

        point_LL = pya.DPoint(-self.side_a/2, -self.side_a/2)
        point_TR = pya.DPoint(self.side_a/2, self.side_a/2)

        ourSquare = pya.DBox(point_LL, point_TR)


#STANDALLONE Testing
if TESTING:
    class klTraining(pya.Library):

        def __init__(self):

            self.description = "klTraining"

            self.layout().register_pcell("TestTraining", TestTraining())

            self.register("klTraining")

    klTraining()           