import pya


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
        


#STANDALLONE Testing
if TESTING:
    class klTraining(pya.Library):

        def __init__(self):

            self.description = "klTraining"

            self.layout().register_pcell("TestTraining", TestTraining())

            self.register("klTraining")

    klTraining()           