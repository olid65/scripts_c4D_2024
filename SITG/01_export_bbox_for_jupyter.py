from typing import Optional
import c4d
import os

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

"""Génère un fichier texte avec la bbox de l'objet sélectionnée si il existe et qu'il a une géométrie
   soit selon la vue de haut
   Le fichier doit être géoréférencé"""

CONTAINER_ORIGIN =1026473

PATH = '/Users/olivierdonze/Documents/TEMP/C4D_BBox'
FN_BBOX = '__bbox_c4d__.txt'

MSG_NO_ORIGIN = "Le document n'est pas géoréférencé, action impossible !"
MSG_NO_CAMERA_PLAN = """Ne fonctionne qu'avec une caméra active en projection "haut" ou avec un objet géométrique sélectionné """
MSG_NO_OBJECT = "Il n' y a pas d'objet sélectionné !"

class Bbox(object):
    def __init__(self,mini,maxi):

        self.min = mini
        self.max = maxi
        self.centre = (self.min+self.max)/2
        self.largeur = self.max.x - self.min.x
        self.hauteur = self.max.z - self.min.z
        self.taille = self.max-self.min

    def intersect(self,bbx2):
        """video explicative sur http://www.youtube.com/watch?v=8b_reDI7iPM"""
        return ( (self.min.x+ self.taille.x)>= bbx2.min.x and
                self.min.x <= (bbx2.min.x + bbx2.taille.x) and
                (self.min.z + self.taille.z) >= bbx2.min.z and
                self.min.z <= (bbx2.min.z + bbx2.taille.z))

    def xInside(self,x):
        """retourne vrai si la variable x est entre xmin et xmax"""
        return x>= self.min.x and x<= self.max.x

    def zInside(self,y):
        """retourne vrai si la variable x est entre xmin et xmax"""
        return y>= self.min.z and y<= self.max.z

    def isInsideX(self,bbox2):
        """renvoie 1 si la bbox est complètement à l'intérier
           renoive 2 si elle est à cheval
           et 0 si à l'extérieur"""
        minInside = self.xInside(bbox2.xmin)
        maxInside = self.xInside(bbox2.xmax)
        if minInside and maxInside : return 1
        if minInside or maxInside : return 2
        #si bbox1 est plus grand
        if bbox2.xmin < self.min.x and bbox2.xmax > self.max.x : return 2
        return 0

    def isInsideZ(self,bbox2):
        """renvoie 1 si la bbox est complètement à l'intérier
           renoive 2 si elle est à cheval
           et 0 si à l'extérieur"""
        minInside = self.zInside(bbox2.ymin)
        maxInside = self.zInside(bbox2.ymax)
        if minInside and maxInside : return 1
        if minInside or maxInside : return 2
        #si bbox1 est plus grand
        if bbox2.ymin < self.min.z and bbox2.ymax > self.max.z : return 2
        return 0

    def ptIsInside(self,pt):
        """renvoie vrai si point c4d est à l'intérieur"""
        return  self.xInside(pt.x) and self.zInside(pt.z)

    def GetSpline(self,origine = c4d.Vector(0)):
        """renvoie une spline c4d de la bbox"""
        res = c4d.SplineObject(4,c4d.SPLINETYPE_LINEAR)
        res[c4d.SPLINEOBJECT_CLOSED] = True
        res.SetAllPoints([c4d.Vector(self.min.x,0,self.max.z)-origine,
                           c4d.Vector(self.max.x,0,self.max.z)-origine,
                           c4d.Vector(self.max.x,0,self.min.z)-origine,
                           c4d.Vector(self.min.x,0,self.min.z)-origine])
        res.Message(c4d.MSG_UPDATE)
        return res
    def __str__(self):
        return f'{self.min.x} {self.min.z} {self.max.x} {self.max.z}'


    @staticmethod
    def fromObj(obj,origine = c4d.Vector()):
        """renvoie la bbox 2d de l'objet"""
        mg = obj.GetMg()

        rad = obj.GetRad()
        centre = obj.GetMp()

        #4 points de la bbox selon orientation de l'objet
        pts = [ c4d.Vector(centre.x+rad.x,centre.y+rad.y,centre.z+rad.z) * mg,
                c4d.Vector(centre.x-rad.x,centre.y+rad.y,centre.z+rad.z) * mg,
                c4d.Vector(centre.x-rad.x,centre.y-rad.y,centre.z+rad.z) * mg,
                c4d.Vector(centre.x-rad.x,centre.y-rad.y,centre.z-rad.z) * mg,
                c4d.Vector(centre.x+rad.x,centre.y-rad.y,centre.z-rad.z) * mg,
                c4d.Vector(centre.x+rad.x,centre.y+rad.y,centre.z-rad.z) * mg,
                c4d.Vector(centre.x-rad.x,centre.y+rad.y,centre.z-rad.z) * mg,
                c4d.Vector(centre.x+rad.x,centre.y-rad.y,centre.z+rad.z) * mg]

        mini = c4d.Vector(min([p.x for p in pts]),min([p.y for p in pts]),min([p.z for p in pts])) + origine
        maxi = c4d.Vector(max([p.x for p in pts]),max([p.y for p in pts]),max([p.z for p in pts])) + origine

        if mini==maxi : return None

        return Bbox(mini,maxi)

    @staticmethod
    def fromView(basedraw,origine = c4d.Vector()):
        dimension = basedraw.GetFrame()
        largeur = dimension["cr"]-dimension["cl"]
        hauteur = dimension["cb"]-dimension["ct"]

        mini =  basedraw.SW(c4d.Vector(0,hauteur,0)) + origine
        maxi = basedraw.SW(c4d.Vector(largeur,0,0)) + origine
        return Bbox(mini,maxi)

def emprise_vue_haut(doc,origin):
    if not origin :
        c4d.gui.MessageDialog(MSG_NO_ORIGIN)
        return
    bd = doc.GetActiveBaseDraw()
    camera = bd.GetSceneCamera(doc)

    if not camera[c4d.CAMERA_PROJECTION]== c4d.Ptop:
        c4d.gui.MessageDialog(MSG_NO_CAMERA_PLAN)
        return
    bbox = Bbox.fromView(bd, origin)
    return bbox

def emprise_objet(obj,origin):
    doc = c4d.documents.GetActiveDocument()
    if not origin :
        c4d.gui.MessageDialog(MSG_NO_ORIGIN)
        return
    bbox = Bbox.fromObj(obj, origin)
    return bbox

def main() -> None:
    origin = doc[CONTAINER_ORIGIN]
    if not origin :
        c4d.gui.MessageDialog(MSG_NO_ORIGIN)
        return
    bbox = None
    if op:
        bbox = emprise_objet(op,origin)

    if not bbox:
        bbox = emprise_vue_haut(doc,origin)

    if bbox:
        #fn = os.path.join(os.path.dirname(__file__),FN_BBOX)
        fn =  os.path.join(PATH,FN_BBOX)

        with open(fn,'w') as f:
            f.write(str(bbox))

    print('le fichier a été généré')

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()