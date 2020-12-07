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

        self.param("fm_tone", self.TypeBoolean, "First Marker Tone", 
                    choices = [["Possitive", True],["Negative", False]],
                    default= True)

        self.param("lo", self.TypeLayer, "Overlay Marker layer", 
                    default = pya.LayerInfo(2, 0, "MarkerOL"))

        self.param("ol_tone", self.TypeBoolean, "Overlay Marker Tone", 
                    choices = [["Possitive", True],["Negative", False]], 
                    default= True)

        self.param("step_name_L", self.TypeString, "Name of aligned step (e.g. 1A)", default = "1A")

        self.param("step_name_OL", self.TypeString, "Name of overlay step (e.g. 3A)", default = "4A") 
        
        self.param("align_type", self.TypeInt, "Alignment type", 
            choices = [["UNSPEC", 0],["TSA", 1], ["BSA", 2]], default= 0) 

        self.param("comment", self.TypeString, "(Optional) Comment (max. 26 char)", default = "")

        self.param("lb_allow", self.TypeBoolean, "Display marker boundary", 
                   choices = [["No", False],["Yes", True]], default= False)

        self.param("lb", self.TypeLayer, "Boundary Marker layer")



        #debuging
        #self.param("debug", self.TypeBoolean, "Debug output", 
        #            choices = [["No", False],["Yes", True]], default= True) 
  
    def display_text_impl(self):
    # Provide a descriptive text for the cell
        return "MA8_AutoMarkSqSq_"+self.step_name_L+"_to_"+self.step_name_OL

    def coerce_parameters_impl(self):
        # TODO: use x to access parameter x and set_x to modify it's value
        rs = None

    def produce_impl(self):
        #Using Double values only - no dbu required (alternatively use scaling instead)
        #dbu definition is only for backwards compatibility with not "D" functions


        # @dataclass
        # class SqinSq:
        #     a : float       = 100.0         #Side lenght of the center square
        #     wall : float    = 10.0          #Wallthickness of the center square FM

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
            markSize : float = 40.0         #Magnification of sign
            markStp : int = 1               #Increment number per long tick
            markTickSep : float = 5.0       #Separation bFalsetween tick and marker 

        
        class HolowSq(pya.Polygon):
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
            def __init__(self, side, wall, dbu = 1):

                self.a = side/2/dbu
                self.h = side/2/dbu-wall/dbu

                self.assign(pya.Polygon(pya.Box(-self.a, -self.a,self.a,self.a)))
                self.insert_hole(pya.Box(-self.h, -self.h,self.h,self.h))

        '''
        Constants and variables:
            DIST_VERNIER : float  - distance of vernier structures center from center of square
            DBU : float - database unit for backwards compatibility
            OL_OVERLAP: float - defines the FM and OL step vernier overlap (-) or gap (+)
            COMMENT_LOC : List : floats -  defines the location of optional comment under
                                            the marker
        '''
        DIST_VERNIER = 200
        DBU = 0.001
        OL_OVERLAP = 0
        COMMENT_LOC = [0,-350]
        ALIGN_LOC = [-DIST_VERNIER,DIST_VERNIER]
        ALIGN_TYPE = ["", "T\\nS\\nA", "B\\nS\\nA"]
        MARK_SIZE = [1000,1000]

        sqFM = HolowSq(200.0, 20.0, DBU)
        sqOL = HolowSq(100.0, 20.0, DBU)
        sqArea = pya.Box(-MARK_SIZE[0]/2/DBU, -MARK_SIZE[0]/2/DBU,
                           MARK_SIZE[1]/2/DBU,  MARK_SIZE[1]/2/DBU)

        _scale = pya.ICplxTrans(1/DBU)

        verniL = Vernier(
                        tLong = 40.0,tShort = 30.0,
                        tWidth = 5.0,sp = 13.0,
                        tCnt = 12,group = 13
                        )

        verniC_OL_B = Vernier(
                        sp = 13.25, asc = True,
                        markers = True, offset = OL_OVERLAP
                        )

        verniC_OL_L = Vernier(
                        sp = 13.25, asc = False,
                        markers = True, offset = OL_OVERLAP
                        )

        verniF_OL_R = Vernier(
                        tWidth = 5.0,sp = 15.1,
                        tCnt = 10,group = 10,
                        markers = True, asc = True,
                        offset = OL_OVERLAP
                        )

        verniF_OL_T = Vernier(
                        tWidth = 5.0,sp = 15.1,
                        tCnt = 10,group = 10,
                        markers = True, asc = False,
                        offset = OL_OVERLAP
                        )



        #Generate vernier array into the cell (layers would be taken from original parameters)
        def vernier_single_gen(param, t = pya.ICplxTrans(0,0), dbu = 1.0):
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
            tick_ln = pya.Box(
                        -param.tWidth/2/dbu,
                        0.0,
                        param.tWidth/2/dbu,
                        param.tLong/dbu)

            tick_sh = pya.Box(
                        -param.tWidth/2/dbu,
                        0.0,
                        param.tWidth/2/dbu,
                        param.tShort/dbu)

            #verniCell = pya.Cell()
            verni_polys = []

            #get the generator direction 
            if param.centered:
                print(param.asc)
                if param.asc:
                    tick_range = range(-param.tCnt, param.tCnt+1, +1)
                    dire = +1
                else:
                    tick_range = range(param.tCnt, -param.tCnt-1, -1)
                    dire = -1
            else:
                if param.asc:
                    tick_range = range(-param.tCnt, 1, +1)
                    dire = +1
                else:
                    tick_range = range(param.tCnt, -1, -1)
                    dire = -1

            for loc in tick_range:
                #loc = tick_range[i]
                t_loc = pya.ICplxTrans(loc * param.sp/dbu, param.offset/dbu)
                if loc % param.group == 0: 
                    #possition of long tick
                    tick_t = tick_ln.transformed(t_loc)
                    tick_t = tick_t.transformed(t)
                    poly = pya.Polygon(tick_t)
                    verni_polys.append(poly)
                    
                    if param.markers:
                        
                        gen = pya.TextGenerator.default_generator()
                        if (loc / param.group * param.markStp) == 0:
                            text = gen.text("0", dbu, param.markSize)
                        else:
                            text = gen.text("{:+.0f}".format(loc / param.group * param.markStp), 
                                       dbu, param.markSize)
                        
                        #text is generated with origin in the LB corner -> corecting by bbox size
                        t_loc_text = pya.ICplxTrans(((dire * loc * param.sp)/dbu 
                                                    - (text.bbox().p2.x)/2), 
                                                    -((text.bbox().p2.y)
                                                    +param.tLong/dbu
                                                    +param.markTickSep/dbu))
                        
                        print(t_loc_text)
                        text_t = text.transformed(t_loc_text)
                        t_text = t.to_trans()
                        #print(t_text)
                        #t_text.disp = t_text.disp / dbu
                        t_text.angle = t_text.angle + 180.0
                        #print(t_text)
                        #verni_polys.append(text_t)
                        verni_polys.append(text_t.transformed(t_text))
                        
                        #TODO: generate marker labels
                else:
                    #position of short tick
                    tick_t = tick_sh.transformed(t_loc)
                    verni_polys.append(pya.Polygon(tick_t.transformed(t)))

            return verni_polys
            

        #lets store objects as regions
        obj_FM_layer = pya.Region()
        obj_OL_layer = pya.Region()
        obj_INV_layer= pya.Region()
        
        #First the squares
        # Square in square structure
        obj_FM_layer.insert(sqFM)
        obj_OL_layer.insert(sqOL)
        obj_INV_layer.insert(sqArea)
            #self.cell.shapes(self.l_layer).insert(sqFM)
            #self.cell.shapes(self.lo_layer).insert(sqOL)

        #depriciated
        verniers_poly = [[],[]]
   
        #Lay step first first:
        rot_matrix = [
                        [0,-1],
                        [1,0],
                        [0,1],
                        [-1,0]
        ]
        
        #First layer vernier markers
        for i in range(0,4):
            t=pya.ICplxTrans(1.0, 90*i, False, 
                            rot_matrix[i][0] * DIST_VERNIER / DBU,
                            rot_matrix[i][1] * DIST_VERNIER / DBU)
            verniers_poly[0].append(vernier_single_gen(verniL, t, DBU))

        #Overlay vernier markers with annotation 
        t=pya.ICplxTrans(1.0, 180+90*0, False, 
                        rot_matrix[0][0] * DIST_VERNIER / DBU,
                        rot_matrix[0][1] * DIST_VERNIER / DBU)
        verniers_poly[1].append(vernier_single_gen(verniC_OL_B, t, DBU))

        t=pya.ICplxTrans(1.0, 180+90*3, False, 
                        rot_matrix[3][0] * DIST_VERNIER / DBU,
                        rot_matrix[3][1] * DIST_VERNIER / DBU)
        verniers_poly[1].append(vernier_single_gen(verniC_OL_L, t, DBU))

        t=pya.ICplxTrans(1.0, 180+90*1, False, 
                        rot_matrix[1][0] * DIST_VERNIER / DBU,
                        rot_matrix[1][1] * DIST_VERNIER / DBU)
        verniers_poly[1].append(vernier_single_gen(verniF_OL_R, t, DBU))
        t=pya.ICplxTrans(1.0, 180+90*2, False, 
                        rot_matrix[2][0] * DIST_VERNIER / DBU,
                        rot_matrix[2][1] * DIST_VERNIER / DBU)
        verniers_poly[1].append(vernier_single_gen(verniF_OL_T, t, DBU))

        for obj in verniers_poly[0]:
            for arr in obj:
              obj_FM_layer.insert(arr)

        for obj in verniers_poly[1]:
            for arr in obj:
              obj_OL_layer.insert(arr)

        #Generate names around the marker (e.g. 2A->1A)
        gen = pya.TextGenerator.default_generator()
        # positive
        stepText = gen.text("{}\\n->\\n{}".format(
                            self.step_name_L,
                            self.step_name_OL), 
                            DBU, 40, False,
                            0, 0, -1)
        #   positive to UR transformation
        t_stepText = pya.ICplxTrans((DIST_VERNIER / DBU - stepText.bbox().p1.x),
                                    (DIST_VERNIER / DBU - stepText.bbox().p1.y))
        obj_FM_layer.insert(stepText.transform(t_stepText))

      
        stepTextInv = gen.text("{}\\n->\\n{}".format(
                            self.step_name_L,
                            self.step_name_OL), 
                            DBU, 40, True,
                            0, 0, -1) 

        obj_OL_layer.insert(stepTextInv.transform(t_stepText))

        #put the alignment indication marker if prefered 
        if self.align_type != 0:
            align_text = gen.text(ALIGN_TYPE[self.align_type], 
                            DBU, 40, False,
                            0, 0, -1)
            align_textInv = gen.text(ALIGN_TYPE[self.align_type], 
                DBU, 40, True,
                0, 0, -1)
        #   positive to UR transformation
            t_align_text = pya.ICplxTrans(ALIGN_LOC[0]/DBU - align_text.bbox().p2.x,
                                        ALIGN_LOC[1]/DBU - align_text.bbox().p1.y)
            obj_FM_layer.insert(align_text.transform(t_align_text))
            obj_OL_layer.insert(align_textInv.transform(t_align_text))
    
        #comment section
        if self.comment != "":
            comment_text = gen.text(self.comment[:25], 
                            DBU, 40, False,
                            0, 0, -1)
            comment_textInv = gen.text(self.comment[:25], 
                            DBU, 40, True,
                            0, 0, -1)
        #   positive to UR transformation
            t_com_text = pya.ICplxTrans((COMMENT_LOC[0]/DBU - comment_text.bbox().center().x),
                                        (COMMENT_LOC[1]/DBU - comment_text.bbox().center().y))
            obj_FM_layer.insert(comment_text.transform(t_com_text))
            obj_OL_layer.insert(comment_textInv.transform(t_com_text))

        #Tone destinqution:
        if self.fm_tone:
            # is possitive
            # used to be >> self.cell.shapes(self.l_layer).insert(obj_FM_layer.transform(_scale))
            self.cell.shapes(self.l_layer).insert(obj_FM_layer)
        else:
            print("tone FM negative")
            obj_neg=obj_INV_layer-obj_FM_layer
            self.cell.shapes(self.l_layer).insert(obj_neg)

        if self.ol_tone:
            # is possitive
            self.cell.shapes(self.lo_layer).insert(obj_OL_layer)
        else:
            print("tone OL negative")
            obj_neg=obj_INV_layer-obj_OL_layer
            self.cell.shapes(self.lo_layer).insert(obj_neg)

        if self.lb_allow:
            self.cell.shapes(self.lb_layer).insert(obj_INV_layer)

class MA8_OverLayVerier(pya.PCellDeclarationHelper):

    def __init__(self):

        # Important: initialize the super class
        super(MA8_OverLayVerier, self).__init__()

        # declare the parameters
        #LayerParameters
        self.param("l", self.TypeLayer, "First Marker layer", 
                    default = pya.LayerInfo(1, 0, "MarkerFM"))

        self.param("fm_tone", self.TypeBoolean, "First Marker Tone", 
                    choices = [["Possitive", True],["Negative", False]],
                    default= True)

        self.param("lo", self.TypeLayer, "Overlay Marker layer", 
                    default = pya.LayerInfo(2, 0, "MarkerOL"))

        self.param("ol_tone", self.TypeBoolean, "Overlay Marker Tone", 
                    choices = [["Possitive", True],["Negative", False]], 
                    default= True)

        self.param("step_name_L", self.TypeString, "Name of aligned step (e.g. 1A)", default = "1A")

        self.param("step_name_OL", self.TypeString, "Name of overlay step (e.g. 3A)", default = "4A") 
        
        self.param("align_type", self.TypeInt, "Alignment type", 
            choices = [["UNSPEC", 0],["TSA", 1], ["BSA", 2]], default= 0) 

        self.param("comment", self.TypeString, "(Optional) Comment (max. 26 char)", default = "")

        self.param("lb_allow", self.TypeBoolean, "Display marker boundary", 
                   choices = [["No", False],["Yes", True]], default= False)

        self.param("lb", self.TypeLayer, "Boundary Marker layer")



        #debuging
        #self.param("debug", self.TypeBoolean, "Debug output", 
        #            choices = [["No", False],["Yes", True]], default= True) 
  
    def display_text_impl(self):
    # Provide a descriptive text for the cell
        return "MA8_AutoMarkSqSq_"+self.step_name_L+"_to_"+self.step_name_OL

    def coerce_parameters_impl(self):
        # TODO: use x to access parameter x and set_x to modify it's value
        rs = None


#STANDALLONE Testing
if TESTING:
    class LithoTesting(pya.Library):

        def __init__(self):

            self.description = "LithoTesting"

            self.layout().register_pcell("MA8_AutoMarkSqSq", MA8_AutoMarkSqSq())

            self.register("LithoTesting")

    LithoTesting()           