import pya

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

        self.assign(pya.DPolygon(pya.DBox(-self.a, -self.a,self.a,self.a))
        self.insert_hole(pya.DBox(-self.h, -self.h,self.h,self.h)
