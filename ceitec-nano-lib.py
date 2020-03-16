import pya
import math
import numpy

from PCell_definition.MEMS.uHotPlate import MicroHotPlateSensor

# class CEITEC_Electrical(pya.Library):

#   def __init__(self):

#     # TODO: change the description
#     self.description = "CEITEC_ElectroMagnetical"

#     # register the PCell declarations
#     # TODO: change the names
#     self.layout().register_pcell("HallBar_regular", HallBar_regular())
#     self.layout().register_pcell("HallBar_Iregular", HallBar_Iregular())
#     self.layout().register_pcell("HallBar_WGNucleator", HallBar_WGNucleator())
#     self.layout().register_pcell("AMR_DiskStructure", AMR_DiskStructure())

#     # TODO: register more PCell declarations

#     # register our library with the name "PCellLib"
#     # TODO: change the library name
#     self.register("CEITEC_Electrical")

class CEITEC_MEMS(pya.Library):

  def __init__(self):

    # TODO: change the description
    self.description = "CEITEC_MEMS"

    # register the PCell declarations
    # TODO: change the names

    self.layout().register_pcell("MicroHotPlate", MicroHotPlateSensor())
    # TODO: register more PCell declarations

    # register our library with the name "PCellLib"
    # TODO: change the library name
    self.register("CEITEC_MEMS")

# class CEITEC_Basic(pya.Library):

#   def __init__(self):

#     # TODO: change the description
#     self.description = "CEITEC_Basic"

#     # register the PCell declarations
#     # TODO: change the names
#     self.layout().register_pcell("ShapeAreaFill", ShapeAreaFill())
#     # TODO: register more PCell declarations

#     # register our library with the name "PCellLib"
#     # TODO: change the library name
#     self.register("CEITEC_Basic")


# CEITEC_Electrical()
# CEITEC_Basic()
CEITEC_MEMS()