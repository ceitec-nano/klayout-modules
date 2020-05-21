import pya
import math
import numpy

class MicroHotPlateSensor(pya.PCellDeclarationHelper):

  def __init__(self):

    # Important: initialize the super class
    super(MicroHotPlateSensor, self).__init__()

    # declare the parameters
    #LayerParameters
    self.param("l", self.TypeLayer, "Hotplate material representation", default = pya.LayerInfo(1, 0, "HotPlateMat"))
    self.param("la", self.TypeLayer, "Hotplate Active Area", default = pya.LayerInfo(99, 500, "HotPlateAct"))
    self.param("ool", self.TypeLayer, "Oxide openings - etch", default = pya.LayerInfo(2,0, "Oxide opening"))
    #self.param("ld", self.TypeLayer, "Describtors layer", default = pya.LayerInfo(99,250))
    self.param("heatl", self.TypeLayer, "Heater material layer", default = pya.LayerInfo(5,0, "Heater"))
    self.param("cntl", self.TypeLayer, "Interconenctions layer", default = pya.LayerInfo(6,0, "Interconnections"))
    self.param("perfl", self.TypeLayer, "Perforation Layer", default = pya.LayerInfo(7, 0, "Perforation"))
    self.param("idcl", self.TypeLayer, "Top electrodes Layer", default = pya.LayerInfo(8,0,"Top IDCs"))
    self.param("lvia", self.TypeLayer, "Vias layer", default = pya.LayerInfo(9,0, "Vias"))
    
    
    #Geometry parameters
    self.param("ovsize", self.TypeList, "Overal size [x, y]", default=[250.0,250.0])
    self.param("size", self.TypeList, "HotPlate Size [x, y]", default = [100.0, 100.0])
    self.param("armLenght", self.TypeDouble, "Arm Lenght", default = 30.0)
    self.param("armWidth", self.TypeDouble, "Arm Width", default = 10.0)
    self.param("actOffset", self.TypeDouble, "Active area offset from edge", default = 5.0)
    self.param("showAct", self.TypeBoolean, "Show active area", choices = [["No", False],["Yes", True]], default= True)
     
    #Process parameters 
    self.param("etchDepth", self.TypeDouble, "Exp. etch depth", default=25.0)
    
    #Heater parameters
    self.param("genHeater", self.TypeBoolean, "Generate Heater", choices = [["No", False],["Yes", True]], default= True)
    self.param("heatType", self.TypeInt, "Heater type", choices = [["Hilbert", 0],["Spiral", 1]], default= 0)
    self.param("heatW", self.TypeDouble, "Heater wire width", default = 1.0)
    self.param("heatOrder", self.TypeInt, "Heater wire Hillbert order", default = 5)
    self.param("heatThick", self.TypeDouble, "Heater wire thickness", default = 0.050)
    #self.param("heatRho", self.TypeDouble, "Active area offset from edge", default = 10.6E-8)
    #self.param("heatRho", self.TypeDouble, "Active area offset from edge", default = 5.0)
    self.param("roundPath", self.TypeBoolean, "Round the heater path", choices = [["No", False],["Yes", True]], default= True)
    self.param("perfAct", self.TypeBoolean, "Perforation of the membrane in Hillbert sq", choices = [["No", False],["Yes", True]], default = True)
    self.param("perfSize", self.TypeDouble, "Perforation size", default = 2.5)

    #wireouts
 
    self.param("genWO", self.TypeBoolean, "Generate Wireouts to overal size", choices = [["No", False],["Yes", True]], default= True) 
    self.param("woW", self.TypeDouble, "Wireout width", default = 5.0)
    self.param("woOP", self.TypeDouble, "Wireout overpass", default = 0.0)

    #contacts
    self.param("genCnt", self.TypeBoolean, "Generate top contacts to overal size", choices = [["No", False],["Yes", True]], default= True) 
    self.param("cntWO", self.TypeDouble, "contact wireout width", default = 10.0)
    self.param("cntW", self.TypeDouble, "contact wire width", default = 1.5)
    self.param("cntB", self.TypeDouble, "contact Bar width", default = 10.0)
    self.param("cntSp", self.TypeDouble, "contact interdigital spacing", default = 1.25)

    #debuging
    self.param("debug", self.TypeBoolean, "Debug output", choices = [["No", False],["Yes", True]], default= True) 
    

    


    #def display_text_impl(self):
        # Provide a descriptive text for the cell
    #return "AMR_Disk(D={:.3f}, AsyV={}".format(self.dia, self.asy_vector)

  def coerce_parameters_impl(self):
    # TODO: use x to access parameter x and set_x to modify it's value
    rs = None
  def produce_impl(self):
    #Calculate layout database unit
    #dbu = self.layout.dbu
    dbu = 1
    size = []
    if len(self.size) < 2:
        if self.debug:
            print("Size < 2 dimension")
        if len(self.size) == 0:
            if self.debug:
                print("paramter size has been adjusted to default - invalid data have provided")
            size = [100.0, 100.0]
        else:
            if self.debug:
                print("Size has been adjusted to {}:{}".format(self.size[0]/dbu, self.size[0]/dbu))
            size.append(float(self.size[0])/dbu)
            size.append(float(self.size[0])/dbu)
    else:
        size.append(float(self.size[0])/dbu)
        size.append(float(self.size[1])/dbu)

    ovSize = []
    if len(self.ovsize) < 2:
        if self.debug:
            print("overal size < 2 dimension")
        if len(self.ovsize) == 0:
            if self.debug:
                print("paramter size has been adjusted to default - invalid data have provided")
            ovSize = [100.0, 100.0]
        else:
            ovSize.append(float(self.ovsize[0])/dbu)
            ovSize.append(float(self.ovsize[0])/dbu)
    else:
        ovSize.append(float(self.ovsize[0])/dbu)
        ovSize.append(float(self.ovsize[1])/dbu)


    armLenght = self.armLenght/dbu
    armWidth = self.armWidth/dbu
    activeArea = [size[0] - self.actOffset, size[1] - self.actOffset]
    woW = self.woW/dbu
    woOP = self.woOP/dbu

    # Membrane Geometry:

    ## arm location on a rectangle = edgeArmOffset
    edgeArmOffset = armWidth / 2 * math.sqrt(2)

    if self.debug:
        print("Size 0:{:.3f}, {}, {}".format(size[0], armLenght, armWidth))
    ## arm starts at following points
    pointArmA = pya.DPoint(size[0]/2 - edgeArmOffset, size[1]/2)
    pointArmD = pya.DPoint(size[0]/2, size[1]/2 - edgeArmOffset)

    ## arm ends in the point P - might be usefull as a connector point
    pointP = pya.DPoint(size[0]/2+armLenght/math.sqrt(2), size[1]/2+armLenght/math.sqrt(2))

    ## arm edge points offsets from the center point P
    armEndPointoffset = armWidth/2/math.sqrt(2)    

    ## Arm edge points in relation to the P point
    
    pointArmB = pya.DPoint(pointP.x-armEndPointoffset, pointP.y+armEndPointoffset)
    pointArmC = pya.DPoint(pointP.x+armEndPointoffset, pointP.y-armEndPointoffset)
    
    ## Lets Try to assemble the membrane as 1/4

    polyPoints = []
    polyPoints.append(pya.DPoint(0.0, 0.0))
    polyPoints.append(pya.DPoint(0.0, size[1]/2))
    polyPoints.append(pointArmA)
    polyPoints.append(pointArmB)
    polyPoints.append(pointArmC)
    polyPoints.append(pointArmD)
    polyPoints.append(pya.DPoint(size[0]/2, 0.0))

    #Lets put it there
    shapeSet = []
    
    Poly = pya.DPolygon(polyPoints)
    shapeSet.append(Poly)
    
    t=pya.DCplxTrans(1.0, 180, False, 0.0, 0.0)
    Poly1 = pya.DPolygon(polyPoints)
    Poly1.transform(t)
    shapeSet.append(Poly1)
        
    t=pya.DCplxTrans(1.0, 0, True, 0.0, 0.0)
    Poly2 = pya.DPolygon(polyPoints)
    Poly2.transform(t)
    shapeSet.append(Poly2)
    
    t=pya.DCplxTrans(1.0, 180, True, 0.0, 0.0)
    Poly3 = pya.DPolygon(polyPoints)
    Poly3.transform(t)
    shapeSet.append(Poly3)
    
    tr=pya.DCplxTrans(1000.0)
    region = pya.Region(shapeSet)
    region.merge()
    region.transform(tr)

    
    self.cell.shapes(self.l_layer).insert(region)

    #Active Area 
    if self.showAct:
        actBox = pya.DBox(-activeArea[0]/2, -activeArea[1]/2, activeArea[0]/2, activeArea[1]/2)
        self.cell.shapes(self.la_layer).insert(actBox)
    
    # Etch area - a rectangele limited by the membrane shape and P point
    etchBox = pya.DBox(-pointP.x, -pointP.y, pointP.x, pointP.y)
    etchRegion = pya.Region(etchBox)
    etchRegion.transform(tr)
    tempRegion = region ^ etchRegion
    etchRegion = tempRegion & etchRegion
    self.cell.shapes(self.ool_layer).insert(etchRegion)

    # Heater wire
    if self.genHeater:
        if self.heatType == 0:
            #Hilbert is defined only for square areas. We would fit whatever is smaller
            
            if activeArea[0] != activeArea[1]:
                if (activeArea[0] > activeArea[1]):
                    wireArea = activeArea[1]/2
                else:
                    wireArea = activeArea[0]/2
            else:
                wireArea = activeArea[0]/2
            
            #issue num2:
            #  the diagonal contact placemnet is required
            #  so we have to calculate space for the return path
            #  segment separation 1sqg => seg = wireArea / 2^n + 1

            Hcnt = 2 ** self.heatOrder + 1
            Hseg = wireArea / (Hcnt)
            print("Hseq: {:.3f}".format(Hseg))
            wireAreaRed = wireArea - Hseg
            a=wireAreaRed+wireAreaRed*1j
            b=wireAreaRed-wireAreaRed*1j
            z = 0

            for i in range(1,self.heatOrder+1):
                w=1j*z.conjugate()
                z = numpy.array([w-a, z-b, z+a, b-w])/2
            z= z.flatten()
            X = [x.real for x in z]
            Y = [x.imag for x in z]

            heatPoints = []

            for i in range (0, len(X)):
                heatPoints.append(pya.DPoint(X[i], Y[i]))

            #lets add the return path
            #  start with calculation of intersection to the beam

            #  linEqa = -1*(pointP.y / pointP.x) - valid only for Square
            #  
            #print("Linear equation is y = {:.3f}.x".format(linEqa))

            heatInitial = heatPoints[0]

            pointS1 = pya.DPoint(-size[0]/2, size[1]/2)
            #pointS2 = pya.DPoint(activeArea[0]/2, -activeArea[1]/2)
            if self.debug:
                print("P:{:.3f},{:.3f} ; S:{:.3f},{:.3f}".format(-pointP.x, pointP.y, pointS1.x, pointS1.y))
            linEqa = (pointP.y-pointS1.y)/(-pointP.x-pointS1.x)
            linEqb = pointP.y - linEqa*-pointP.x 
            if self.debug:
                print("Line equation is: y={:.3f}x+{:.3f}".format(linEqa,linEqb))

            heatPoints.insert(0, pya.DPoint(heatPoints[0].x - 2*Hseg, heatPoints[0].y))
            heatPoints.insert(0, pya.DPoint(heatPoints[0].x, linEqa*(heatPoints[0].x+Hseg)+linEqb))
            heatPoints.append(pya.DPoint(heatPoints[len(heatPoints)-1].x, \
                linEqa*(heatPoints[len(heatPoints)-1].x+Hseg)-linEqb))

            heatPoints.append(pya.DPoint(pointP.x - Hseg, -pointP.y)) #arm contacts
            heatPoints.insert(0, pya.DPoint(-pointP.x - Hseg, pointP.y))
            
            #probably somewhere here is a good time to calculate perforations 
            # teoretically first opening should be -Heg/2 to the left of the very first 
            # point and should repeat in X and Y axis with interval of Hseg
            # 

            # center is HeatPoints[2] -Hseg/2 ?
            if self.perfAct:
                perfW = self.perfSize/2 / dbu
                #perfCenter = pya.DPoint(heatPoints[2].x - Hseg, heatPoints[2].y - Hseg)
                #perfBox = pya.DBox(perfCenter.x-perfW, perfCenter.y-perfW, perfCenter.x+perfW, perfCenter.y-perfW)
                elCell = self.layout.create_cell("Perforator")
                perfBox = pya.DPolygon(pya.DBox(-perfW, -perfW, perfW, perfW))
                if self.roundPath:
                    perfBox = perfBox.round_corners(Hseg/2, Hseg/2, 32)
                elCell.shapes(self.perfl_layer).insert(perfBox)

                #lets make an array of them 
                x_vect = pya.DVector(2*Hseg, 0.0)
                y_vect = pya.DVector(0.0, 2*Hseg)
                t = pya.DCplxTrans(heatInitial.x, heatInitial.y+Hseg)
                perfArr = pya.DCellInstArray(elCell.cell_index(), t, x_vect, y_vect, Hcnt-1, Hcnt-2)

                self.cell.insert(perfArr)

                #move to the right coordinates
                pathT = pya.DCplxTrans(Hseg, 0)
                heatPath = pya.DPath(heatPoints, self.heatW)
                heatPathT = heatPath.transformed(pathT)
                if self.roundPath:
                    heatPathT = heatPath.round_corners(Hseg/2,32, 0.001)
                    heatCenter = heatPathT.bbox().center()
                    print(heatCenter)
                    print("Rounded Path center: {}:{}".format(heatCenter.x, heatCenter.y))
                    pathTr = pya.DCplxTrans(-heatCenter.x, -heatCenter.y)
                    heatPathT = heatPathT.transformed(pathTr)
                self.cell.shapes(self.heatl_layer).insert(heatPathT)        
        else:
            print("Wire definition has not been found!")
            #TODO ... other types of heaters

    if self.genWO:
        #we would make a wire connection from the P point to the edge of the membrane 
        # overpass on both sides as an option

        # it has to be realized as a set of the 4 path
        print("Overal size: {}:{}".format(ovSize[0], ovSize[1]))
        woPathA = pya.DPath([pointP, pya.DPoint(ovSize[0]/2, ovSize[1]/2)],woW, woOP, woOP)
        woPathB = pya.DPath([pya.DPoint(-pointP.x, pointP.y), pya.DPoint(-ovSize[0]/2, ovSize[1]/2)],\
            woW, woOP, woOP)
        woPathC = pya.DPath([pya.DPoint(-pointP.x, -pointP.y), pya.DPoint(-ovSize[0]/2, -ovSize[1]/2)],\
            woW, woOP, woOP)
        woPathD = pya.DPath([pya.DPoint(pointP.x, -pointP.y), pya.DPoint(ovSize[0]/2, -ovSize[1]/2)],\
            woW, woOP, woOP)
        self.cell.shapes(self.cntl_layer).insert(woPathA)
        self.cell.shapes(self.cntl_layer).insert(woPathB)  
        self.cell.shapes(self.cntl_layer).insert(woPathC)  
        self.cell.shapes(self.cntl_layer).insert(woPathD)  
    
    if self.genCnt:
        # Ok that would be fun ... 
        #   so at first we should be able to find how many of the IGC we would be able to fit
        #   in between of the perforations (maybe we should count also for the minimal separation)
        #   principally:
        #       single IGS pair consists of 2 wires and 2 gaps = IGSpairW?
        #       testing condition is therefore IGSCnt = floor((Hseg - perfW) / IGSpairW)
        cntW = self.cntW / dbu
        cntSp = self.cntSp / dbu
        cntB = self.cntB / dbu
        cntBunchW = 2*(cntW+cntSp)
        cntCnt = math.floor((2*Hseg-2*perfW)/cntBunchW)
        if self.debug:
            print("IDC W={}".format(cntBunchW))
            print("IDCs per bunch: {}".format(cntCnt))
        if cntCnt == 0:
            print("Error: Interdigital contacts with given specs could not be realized because of geometric containts!")
        else:
            #lets make a subcell with interdigital pair
            #   so first calculate the active area - contact bars to get the lenght
            #   contacts singles
            cntCell = self.layout.create_cell("IDC_subcell")
            cntArrCell = self.layout.create_cell("IDC_cell")

            #cntLenght = activeArea - 2*cntB - cntSp

            cntPath_p1 = pya.DPoint((cntSp+cntW)/2, activeArea[1]/2-cntB)
            cntPath_p2 = pya.DPoint((cntSp+cntW)/2, -activeArea[1]/2+cntSp+cntB) #TODO tohle je asi blbe ... 
            cntPath_pA =  [cntPath_p1, cntPath_p2]
            cntPath_pB =  [cntPath_p1 * -1, cntPath_p2 * -1]
            
            cntPath_A = pya.DPath(cntPath_pA, cntW, 0.0, 0.0)
            cntPath_B = pya.DPath(cntPath_pB, cntW, 0.0, 0.0)

            cntCell.shapes(self.idcl_layer).insert(cntPath_A)
            cntCell.shapes(self.idcl_layer).insert(cntPath_B)

            #now lets make bunches of cntCnt and center them 
            # TODO: tady jsem skoncil ... potreba projit odstavec pod
            #BEGIN
            x_vect = pya.DVector(cntBunchW, 0.0)
            y_vect = pya.DVector(0.0, 0.0)
            if self.debug:
                print("IDC bunch Vectors: {}, {}, {}, {}".format(\
                    x_vect.x, x_vect.y, y_vect.x, y_vect.y))
            t = pya.DCplxTrans(0, 0)
            cntArr = pya.DCellInstArray(cntCell.cell_index(), t, x_vect, y_vect, cntCnt, 1)
            
            #center the origins on top of each other
            #   here we have a bunch of IDCs
            cntArr_center = cntArr.bbox(self.layout).center()
            if self.debug:
                print("Bunch center: {},{}".format(cntArr_center.x, cntArr_center.y))
            t=pya.DCplxTrans(1.0, 0, False, -cntArr_center.x, -cntArr_center.y)
            cntArr.transform(t)
            cntArrCell.insert(cntArr)
            
            #   move the array to the position of Hilb. initial and paste it into the overal array
            
            a_vect = pya.DVector(2*Hseg, 0.0)
            b_vect = pya.DVector(0.0, 0.0)

            cntLoct = pya.DCplxTrans(1.0,0,False, heatInitial.x-Hseg, 0.0)

            cntArrAll = pya.DCellInstArray(cntArrCell.cell_index(), cntLoct, a_vect, b_vect, Hcnt, 1)
            self.cell.insert(cntArrAll)

            #Top and bottom contact 
            #  by principle the bar-contact should be horizontally oriented across the active zone
            #  then they should continue to the respective P-points (upright, lowerleft)
            

            #  Contact bar would be a box from the edge to the edge of active area with a width of 
            #  cntB 

            # pointCNT1A = pya.DPoint(activeArea[0]/2, activeArea[1]/2)

            # if self.debug:
            #     print("P:{:.3f},{:.3f} ; CNT:{:.3f},{:.3f}".format(-pointP.x, pointP.y, pointCNT1A.x, pointCNT1A.y))
            # linCntEqa = (pointP.y-pointCNT1A.y)/(-pointP.x-pointCNT1A.x)
            # linCntEqb = pointP.y - linCntEqa*-pointP.x 

            # if self.debug:
            #     print("CNT line equation is: y={:.3f}x+{:.3f}".format(linEqa,linEqb))
            
            # pointCNT1B =




            # Contact Bars
            cntBarW = self.cntB/dbu
            cntWoW = self.cntWO/dbu
            shapeSetCNT = []
            #cntBarA 
            shapeSetCNT.append(pya.DBox(-activeArea[0]/2, activeArea[1]/2-cntBarW,\
                activeArea[0]/2, activeArea[1]/2))
            #cntBarB
            shapeSetCNT.append(pya.DBox(-activeArea[0]/2, -activeArea[1]/2,\
                activeArea[0]/2, -activeArea[1]/2+cntBarW))

            pointS2 = pya.DPoint(activeArea[0]/2, activeArea[1]/2)
            #cntWOPathA
            shapeSetCNT.append(pya.DPath([pointS2,pointP], cntWoW, cntWoW/2, cntWoW).polygon())
            #cntWOPathB
            shapeSetCNT.append(pya.DPath([-pointS2,-pointP], cntWoW, cntWoW/2, cntWoW).polygon())

            for shape in shapeSetCNT:
                self.cell.shapes(self.idcl_layer).insert(shape)

            #Vias 
            #TODO: repair position of the vias

            cntViaW = cntWoW * 0.9/2 # 10% smaller then the wire
            tr = pya.DCplxTrans(1.0, 45.0, False, pya.DVector(pointP))
            cntViaA = pya.DPolygon(pya.DBox(-cntViaW, -cntViaW,\
                cntViaW, cntViaW)).transform(tr)
            tr = pya.DCplxTrans(1.0, 45.0, False, pya.DVector(-pointP))
            cntViaB = pya.DPolygon(pya.DBox(-cntViaW, -cntViaW,\
                cntViaW, cntViaW)).transformed(tr)
            self.cell.shapes(self.lvia_layer).insert(cntViaA)
            self.cell.shapes(self.lvia_layer).insert(cntViaB)
            
            
            
            #tr=pya.DCplxTrans(1000.0)
            #regionCNT = pya.Region(shapeSetCNT)
            #regionCNT.merge()
            #regionCNT.transform(tr)
            # not working -- some expansion happening there. 
            
            
            

                        
            #END


        
          

        #elCell.shapes(self.perfl_layer).insert(perfBox)

        #lets make an array of them 
        #x_vect = pya.DVector(Hseg, 0.0)
        #y_vect = pya.DVector(0.0, Hseg)
        #t = pya.DCplxTrans(0, 0)
        #perfArr = pya.DCellInstArray(elCell.cell_index(), t, x_vect, y_vect, Hcnt, Hcnt)

        #self.cell.insert(perfArr)


class MicroHotPlateSensorHK(pya.PCellDeclarationHelper):

  def __init__(self):

    # Important: initialize the super class
    super(MicroHotPlateSensorHK, self).__init__()

    # declare the parameters
    #LayerParameters
    self.param("l", self.TypeLayer, "Hotplate material representation", default = pya.LayerInfo(1, 0, "HotPlateMat"))
    self.param("la", self.TypeLayer, "Hotplate Active Area", default = pya.LayerInfo(99, 0, "HotPlateAct"))
    self.param("loa", self.TypeLayer, "Hotplate Overal Area", default = pya.LayerInfo(99, 500, "uHotPlate_Overal"))
    self.param("ool", self.TypeLayer, "Oxide openings - etch", default = pya.LayerInfo(2,0, "Oxide opening"))
    #self.param("ld", self.TypeLayer, "Describtors layer", default = pya.LayerInfo(99,250))
    self.param("heatl", self.TypeLayer, "Heater material layer", default = pya.LayerInfo(5,0, "Heater wires"))
    #self.param("cntl", self.TypeLayer, "Interconenctions layer", default = pya.LayerInfo(6,0, "Interconnections"))
    #self.param("perfl", self.TypeLayer, "Perforation Layer", default = pya.LayerInfo(7, 0, "Perforation"))
    #self.param("idcl", self.TypeLayer, "Top electrodes Layer", default = pya.LayerInfo(8,0,"Top IDCs"))
    #self.param("lvia", self.TypeLayer, "Vias layer", default = pya.LayerInfo(9,0, "Vias"))
    
    
    #Geometry parameters
    self.param("ovsize", self.TypeList, "Overal size [x, y]", default=[250.0,250.0])
    self.param("size", self.TypeList, "HotPlate Size [x, y]", default = [100.0, 100.0])
    #self.param("armLenght", self.TypeDouble, "Arm Lenght", default = 30.0)
    self.param("armWidth", self.TypeDouble, "Arm Width", default = 10.0)
    #self.param("armWidth", self.TypeDouble, "Beam to Membrane separation", default = 30.0)
    self.param("armBMS", self.TypeDouble, "Beam to Side separation", default = 10.0)
    self.param("actOffset", self.TypeDouble, "Active area offset from edge", default = 5.0)
    self.param("showAct", self.TypeBoolean, "Show active area", choices = [["No", False],["Yes", True]], default= True)
     
    #Process parameters 
    self.param("etchDepth", self.TypeDouble, "Exp. etch depth", default=25.0)
    
    #Heater parameters
    self.param("genHeater", self.TypeBoolean, "Generate Heater", choices = [["No", False],["Yes", True]], default= True)
    self.param("heatType", self.TypeInt, "Heater type", choices = [["Hilbert", 0],["Meander", 1],["Spiral", 2]], default= 0)
    #self.param("heatW", self.TypeDouble, "Heater wire width", default = 1.0)
    #self.param("heatOrder", self.TypeInt, "Heater wire Hillbert order", default = 5)
    #self.param("heatThick", self.TypeDouble, "Heater wire thickness", default = 0.050)
    #self.param("heatRho", self.TypeDouble, "Active area offset from edge", default = 10.6E-8)
    #self.param("heatRho", self.TypeDouble, "Active area offset from edge", default = 5.0)
    #self.param("roundPath", self.TypeBoolean, "Round the heater path", choices = [["No", False],["Yes", True]], default= True)
    #self.param("perfAct", self.TypeBoolean, "Perforation of the membrane in Hillbert sq", choices = [["No", False],["Yes", True]], default = True)
    #self.param("perfSize", self.TypeDouble, "Perforation size", default = 2.5)

    #wireouts
 
    #self.param("genWO", self.TypeBoolean, "Generate Wireouts to overal size", choices = [["No", False],["Yes", True]], default= True) 
    #self.param("woW", self.TypeDouble, "Wireout width", default = 5.0)
    #self.param("woOP", self.TypeDouble, "Wireout overpass", default = 0.0)

    #contacts
    #self.param("genCnt", self.TypeBoolean, "Generate top contacts to overal size", choices = [["No", False],["Yes", True]], default= True) 
    #self.param("cntWO", self.TypeDouble, "contact wireout width", default = 10.0)
    #self.param("cntW", self.TypeDouble, "contact wire width", default = 1.5)
    #self.param("cntB", self.TypeDouble, "contact Bar width", default = 10.0)
    #self.param("cntSp", self.TypeDouble, "contact interdigital spacing", default = 1.25)

    #debuging
    self.param("debug", self.TypeBoolean, "Debug output", choices = [["No", False],["Yes", True]], default= True) 
    

    


    #def display_text_impl(self):
        # Provide a descriptive text for the cell
    #return "AMR_Disk(D={:.3f}, AsyV={}".format(self.dia, self.asy_vector)

  def coerce_parameters_impl(self):
    # TODO: use x to access parameter x and set_x to modify it's value
    rs = None
  def produce_impl(self):
    size = []
    if len(self.size) < 2:
        if self.debug:
            print("Size < 2 dimension")
        if len(self.size) == 0:
            if self.debug:
                print("paramter size has been adjusted to default - invalid data have provided")
            size = [100.0, 100.0]
        else:
            if self.debug:
                print("Size has been adjusted to {}:{}".format(self.size[0]/dbu, self.size[0]/dbu))
            size.append(float(self.size[0]))
            size.append(float(self.size[0]))
    else:
        size.append(float(self.size[0]))
        size.append(float(self.size[1]))

    ovSize = []
    if len(self.ovsize) < 2:
        if self.debug:
            print("overal size < 2 dimension")
        if len(self.ovsize) == 0:
            if self.debug:
                print("paramter size has been adjusted to default - invalid data have provided")
            ovSize = [100.0, 100.0]
        else:
            ovSize.append(float(self.ovsize[0]))
            ovSize.append(float(self.ovsize[0]))
    else:
        ovSize.append(float(self.ovsize[0]))
        ovSize.append(float(self.ovsize[1]))




    #armLenght = self.armLenght
    armWidth = self.armWidth
    armBSS = self.armBMS
    activeArea = [size[0] - self.actOffset, size[1] - self.actOffset]
    #woW = self.woW/dbu
    #woOP = self.woOP/dbu

    # Membrane Geometry:
    memParts=[]
    #   Firstly generate the centerpart
    memCenter = pya.Polygon(pya.DPolygon(pya.DBox(-size[0]/2, -size[1]/2, size[0]/2, size[1]/2)))
    memParts.append(memParts)
    #   Time for beams
    #   Calculate the BeamArmcenter to the membrane edge, alias beam to memrane spacing
    memBMS = [(ovSize[0]-size[0]/2) -armBSS -armWidth/2,\
        (ovSize[1]-size[1]/2) -armBSS -armWidth/2]

    memBeam1 = pya.Polygon(pya.DPath([\
        pya.DPoint((size[0]-armWidth)/2, size[1]/2),\
        pya.DPoint((size[0]-armWidth)/2, size[1]/2+memBMS[1]),\
        pya.DPoint(-ovSize[0]/2, size[1]/2+memBMS[1])], armWidth).polygon())
    memParts.append(memBeam1)

    memBeam2 = pya.Polygon(pya.DPath([\
        pya.DPoint(-size[0]/2, (size[1]/2)-armWidth/2),\
        pya.DPoint(-size[0]-memBMS[0], size[1]/2-armWidth/2),\
        pya.DPoint(-size[0]-memBMS[0], -ovSize[1]/2)], armWidth).polygon())
    memParts.append(memBeam2)

    memBeam3 = pya.Polygon(pya.DPath([\
        pya.DPoint((-size[0]+armWidth)/2, -size[1]/2),\
        pya.DPoint((-size[0]+armWidth)/2, -size[1]/2-memBMS[1]),\
        pya.DPoint(ovSize[0]/2, -size[1]/2-memBMS[1])], armWidth).polygon())
    memParts.append(memBeam3)

    memBeam4 = pya.Polygon(pya.DPath([\
        pya.DPoint(size[0]/2, (-size[1]-armWidth)/2),\
        pya.DPoint(size[0]+memBMS[0], -size[1]/2+armWidth/2),\
        pya.DPoint(size[0]+memBMS[0], ovSize[1]/2)], armWidth).polygon())
    memParts.append(memBeam4)

    #here it would be probably useful to put them all into one polygon object (hopefully it\
    # would work ;))
    if self.debug:
        print(memParts)
        for member in memParts:
            self.cell.shapes(self.l_layer).insert(member)
    tr=pya.DCplxTrans(1000.0) #workaround for difference in DBU
    region = pya.Region(memParts)
    region.merge()
    region.transform(tr)   
    self.cell.shapes(self.l_layer).insert(region)
    
    #Active Area
    actBox = pya.DBox(-activeArea[0]/2, -activeArea[1]/2,\
         activeArea[0]/2, activeArea[1]/2)
    if self.showAct:
        self.cell.shapes(self.la_layer).insert(actBox)
    
    # Etch area - in this variant the overal size of membrane
    etchRegion = pya.Region(actBox)
    etchRegion.transform(tr)
    
    tempRegion = region ^ etchRegion
    etchRegion = tempRegion & etchRegion
    self.cell.shapes(self.ool_layer).insert(etchRegion)

    # Heater wire
    # if self.genHeater:
    #     if self.heatType == 0:
    #         #Hilbert is defined only for square areas. We would fit whatever is smaller
            
    #         if activeArea[0] != activeArea[1]:
    #             if (activeArea[0] > activeArea[1]):
    #                 wireArea = activeArea[1]/2
    #             else:
    #                 wireArea = activeArea[0]/2
    #         else:
    #             wireArea = activeArea[0]/2
            
    #         #issue num2:
    #         #  the diagonal contact placemnet is required
    #         #  so we have to calculate space for the return path
    #         #  segment separation 1sqg => seg = wireArea / 2^n + 1

    #         Hcnt = 2 ** self.heatOrder + 1
    #         Hseg = wireArea / (Hcnt)
    #         print("Hseq: {:.3f}".format(Hseg))
    #         wireAreaRed = wireArea - Hseg
    #         a=wireAreaRed+wireAreaRed*1j
    #         b=wireAreaRed-wireAreaRed*1j
    #         z = 0

    #         for i in range(1,self.heatOrder+1):
    #             w=1j*z.conjugate()
    #             z = numpy.array([w-a, z-b, z+a, b-w])/2
    #         z= z.flatten()
    #         X = [x.real for x in z]
    #         Y = [x.imag for x in z]

    #         heatPoints = []

    #         for i in range (0, len(X)):
    #             heatPoints.append(pya.DPoint(X[i], Y[i]))

    #         #lets add the return path
    #         #  start with calculation of intersection to the beam

    #         #  linEqa = -1*(pointP.y / pointP.x) - valid only for Square
    #         #  
    #         #print("Linear equation is y = {:.3f}.x".format(linEqa))

    #         heatInitial = heatPoints[0]

    #         pointS1 = pya.DPoint(-size[0]/2, size[1]/2)
    #         #pointS2 = pya.DPoint(activeArea[0]/2, -activeArea[1]/2)
    #         if self.debug:
    #             print("P:{:.3f},{:.3f} ; S:{:.3f},{:.3f}".format(-pointP.x, pointP.y, pointS1.x, pointS1.y))
    #         linEqa = (pointP.y-pointS1.y)/(-pointP.x-pointS1.x)
    #         linEqb = pointP.y - linEqa*-pointP.x 
    #         if self.debug:
    #             print("Line equation is: y={:.3f}x+{:.3f}".format(linEqa,linEqb))

    #         heatPoints.insert(0, pya.DPoint(heatPoints[0].x - 2*Hseg, heatPoints[0].y))
    #         heatPoints.insert(0, pya.DPoint(heatPoints[0].x, linEqa*(heatPoints[0].x+Hseg)+linEqb))
    #         heatPoints.append(pya.DPoint(heatPoints[len(heatPoints)-1].x, \
    #             linEqa*(heatPoints[len(heatPoints)-1].x+Hseg)-linEqb))

    #         heatPoints.append(pya.DPoint(pointP.x - Hseg, -pointP.y)) #arm contacts
    #         heatPoints.insert(0, pya.DPoint(-pointP.x - Hseg, pointP.y))
            
    #         #probably somewhere here is a good time to calculate perforations 
    #         # teoretically first opening should be -Heg/2 to the left of the very first 
    #         # point and should repeat in X and Y axis with interval of Hseg
    #         # 

    #         # center is HeatPoints[2] -Hseg/2 ?
    #         if self.perfAct:
    #             perfW = self.perfSize/2 / dbu
    #             #perfCenter = pya.DPoint(heatPoints[2].x - Hseg, heatPoints[2].y - Hseg)
    #             #perfBox = pya.DBox(perfCenter.x-perfW, perfCenter.y-perfW, perfCenter.x+perfW, perfCenter.y-perfW)
    #             elCell = self.layout.create_cell("Perforator")
    #             perfBox = pya.DPolygon(pya.DBox(-perfW, -perfW, perfW, perfW))
    #             if self.roundPath:
    #                 perfBox = perfBox.round_corners(Hseg/2, Hseg/2, 32)
    #             elCell.shapes(self.perfl_layer).insert(perfBox)

    #             #lets make an array of them 
    #             x_vect = pya.DVector(2*Hseg, 0.0)
    #             y_vect = pya.DVector(0.0, 2*Hseg)
    #             t = pya.DCplxTrans(heatInitial.x, heatInitial.y+Hseg)
    #             perfArr = pya.DCellInstArray(elCell.cell_index(), t, x_vect, y_vect, Hcnt-1, Hcnt-2)

    #             self.cell.insert(perfArr)

    #             #move to the right coordinates
    #             pathT = pya.DCplxTrans(Hseg, 0)
    #             heatPath = pya.DPath(heatPoints, self.heatW)
    #             heatPathT = heatPath.transformed(pathT)
    #             if self.roundPath:
    #                 heatPathT = heatPath.round_corners(Hseg/2,32, 0.001)
    #                 heatCenter = heatPathT.bbox().center()
    #                 print(heatCenter)
    #                 print("Rounded Path center: {}:{}".format(heatCenter.x, heatCenter.y))
    #                 pathTr = pya.DCplxTrans(-heatCenter.x, -heatCenter.y)
    #                 heatPathT = heatPathT.transformed(pathTr)
    #             self.cell.shapes(self.heatl_layer).insert(heatPathT)        
    #     else:
    #         print("Wire definition has not been found!")
    #         #TODO ... other types of heaters

    # if self.genWO:
    #     #we would make a wire connection from the P point to the edge of the membrane 
    #     # overpass on both sides as an option

    #     # it has to be realized as a set of the 4 path
    #     print("Overal size: {}:{}".format(ovSize[0], ovSize[1]))
    #     woPathA = pya.DPath([pointP, pya.DPoint(ovSize[0]/2, ovSize[1]/2)],woW, woOP, woOP)
    #     woPathB = pya.DPath([pya.DPoint(-pointP.x, pointP.y), pya.DPoint(-ovSize[0]/2, ovSize[1]/2)],\
    #         woW, woOP, woOP)
    #     woPathC = pya.DPath([pya.DPoint(-pointP.x, -pointP.y), pya.DPoint(-ovSize[0]/2, -ovSize[1]/2)],\
    #         woW, woOP, woOP)
    #     woPathD = pya.DPath([pya.DPoint(pointP.x, -pointP.y), pya.DPoint(ovSize[0]/2, -ovSize[1]/2)],\
    #         woW, woOP, woOP)
    #     self.cell.shapes(self.cntl_layer).insert(woPathA)
    #     self.cell.shapes(self.cntl_layer).insert(woPathB)  
    #     self.cell.shapes(self.cntl_layer).insert(woPathC)  
    #     self.cell.shapes(self.cntl_layer).insert(woPathD)  
    
    # if self.genCnt:
        # Ok that would be fun ... 
        #   so at first we should be able to find how many of the IGC we would be able to fit
        #   in between of the perforations (maybe we should count also for the minimal separation)
        #   principally:
        #       single IGS pair consists of 2 wires and 2 gaps = IGSpairW?
        #       testing condition is therefore IGSCnt = floor((Hseg - perfW) / IGSpairW)
        # cntW = self.cntW / dbu
        # cntSp = self.cntSp / dbu
        # cntB = self.cntB / dbu
        # cntBunchW = 2*(cntW+cntSp)
        # cntCnt = math.floor((2*Hseg-2*perfW)/cntBunchW)
        # if self.debug:
        #     print("IDC W={}".format(cntBunchW))
        #     print("IDCs per bunch: {}".format(cntCnt))
        # if cntCnt == 0:
        #     print("Error: Interdigital contacts with given specs could not be realized because of geometric containts!")
        # else:
        #     #lets make a subcell with interdigital pair
        #     #   so first calculate the active area - contact bars to get the lenght
        #     #   contacts singles
        #     cntCell = self.layout.create_cell("IDC_subcell")
        #     cntArrCell = self.layout.create_cell("IDC_cell")

        #     #cntLenght = activeArea - 2*cntB - cntSp

        #     cntPath_p1 = pya.DPoint((cntSp+cntW)/2, activeArea[1]/2-cntB)
        #     cntPath_p2 = pya.DPoint((cntSp+cntW)/2, -activeArea[1]/2+cntSp+cntB) #TODO tohle je asi blbe ... 
        #     cntPath_pA =  [cntPath_p1, cntPath_p2]
        #     cntPath_pB =  [cntPath_p1 * -1, cntPath_p2 * -1]
            
        #     cntPath_A = pya.DPath(cntPath_pA, cntW, 0.0, 0.0)
        #     cntPath_B = pya.DPath(cntPath_pB, cntW, 0.0, 0.0)

        #     cntCell.shapes(self.idcl_layer).insert(cntPath_A)
        #     cntCell.shapes(self.idcl_layer).insert(cntPath_B)

        #     #now lets make bunches of cntCnt and center them 
        #     # TODO: tady jsem skoncil ... potreba projit odstavec pod
        #     #BEGIN
        #     x_vect = pya.DVector(cntBunchW, 0.0)
        #     y_vect = pya.DVector(0.0, 0.0)
        #     if self.debug:
        #         print("IDC bunch Vectors: {}, {}, {}, {}".format(\
        #             x_vect.x, x_vect.y, y_vect.x, y_vect.y))
        #     t = pya.DCplxTrans(0, 0)
        #     cntArr = pya.DCellInstArray(cntCell.cell_index(), t, x_vect, y_vect, cntCnt, 1)
            
        #     #center the origins on top of each other
        #     #   here we have a bunch of IDCs
        #     cntArr_center = cntArr.bbox(self.layout).center()
        #     if self.debug:
        #         print("Bunch center: {},{}".format(cntArr_center.x, cntArr_center.y))
        #     t=pya.DCplxTrans(1.0, 0, False, -cntArr_center.x, -cntArr_center.y)
        #     cntArr.transform(t)
        #     cntArrCell.insert(cntArr)
            
        #     #   move the array to the position of Hilb. initial and paste it into the overal array
            
        #     a_vect = pya.DVector(2*Hseg, 0.0)
        #     b_vect = pya.DVector(0.0, 0.0)

        #     cntLoct = pya.DCplxTrans(1.0,0,False, heatInitial.x-Hseg, 0.0)

        #     cntArrAll = pya.DCellInstArray(cntArrCell.cell_index(), cntLoct, a_vect, b_vect, Hcnt, 1)
        #     self.cell.insert(cntArrAll)

        #     #Top and bottom contact 
        #     #  by principle the bar-contact should be horizontally oriented across the active zone
        #     #  then they should continue to the respective P-points (upright, lowerleft)
            

        #     #  Contact bar would be a box from the edge to the edge of active area with a width of 
        #     #  cntB 

        #     # pointCNT1A = pya.DPoint(activeArea[0]/2, activeArea[1]/2)

        #     # if self.debug:
        #     #     print("P:{:.3f},{:.3f} ; CNT:{:.3f},{:.3f}".format(-pointP.x, pointP.y, pointCNT1A.x, pointCNT1A.y))
        #     # linCntEqa = (pointP.y-pointCNT1A.y)/(-pointP.x-pointCNT1A.x)
        #     # linCntEqb = pointP.y - linCntEqa*-pointP.x 

        #     # if self.debug:
        #     #     print("CNT line equation is: y={:.3f}x+{:.3f}".format(linEqa,linEqb))
            
        #     # pointCNT1B =




        #     # Contact Bars
        #     cntBarW = self.cntB/dbu
        #     cntWoW = self.cntWO/dbu
        #     shapeSetCNT = []
        #     #cntBarA 
        #     shapeSetCNT.append(pya.DBox(-activeArea[0]/2, activeArea[1]/2-cntBarW,\
        #         activeArea[0]/2, activeArea[1]/2))
        #     #cntBarB
        #     shapeSetCNT.append(pya.DBox(-activeArea[0]/2, -activeArea[1]/2,\
        #         activeArea[0]/2, -activeArea[1]/2+cntBarW))

        #     pointS2 = pya.DPoint(activeArea[0]/2, activeArea[1]/2)
        #     #cntWOPathA
        #     shapeSetCNT.append(pya.DPath([pointS2,pointP], cntWoW, cntWoW/2, cntWoW).polygon())
        #     #cntWOPathB
        #     shapeSetCNT.append(pya.DPath([-pointS2,-pointP], cntWoW, cntWoW/2, cntWoW).polygon())

        #     for shape in shapeSetCNT:
        #         self.cell.shapes(self.idcl_layer).insert(shape)

        #     #Vias 
        #     #TODO: repair position of the vias

        #     cntViaW = cntWoW * 0.9/2 # 10% smaller then the wire
        #     tr = pya.DCplxTrans(1.0, 45.0, False, pya.DVector(pointP))
        #     cntViaA = pya.DPolygon(pya.DBox(-cntViaW, -cntViaW,\
        #         cntViaW, cntViaW)).transform(tr)
        #     tr = pya.DCplxTrans(1.0, 45.0, False, pya.DVector(-pointP))
        #     cntViaB = pya.DPolygon(pya.DBox(-cntViaW, -cntViaW,\
        #         cntViaW, cntViaW)).transformed(tr)
        #     self.cell.shapes(self.lvia_layer).insert(cntViaA)
        #     self.cell.shapes(self.lvia_layer).insert(cntViaB) 