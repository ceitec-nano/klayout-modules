# $autorun
import pya
import math
import numpy

#Temporary
import sys
print(sys.path)
sys.path.insert(0,"/home/sadilek/.klayout/pymacros/klayout-modules")
from PCell_definition.MEMS.uHotPlate import MicroHotPlateSensor
from PCell_definition.MEMS.uHotPlate import MicroHotPlateSensorHK

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
    self.layout().register_pcell("MicroHotPlateHK", MicroHotPlateSensorHK())
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