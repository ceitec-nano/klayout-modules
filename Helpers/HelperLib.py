import pya

    class HolowSq:
        def __init__(self, side, wall):
            self.a = side
            self.w = wall
        def shape():
            poly = pya.DBox(-self.a/2, -self.a/2,self.a/2,self.a/2).polygon()