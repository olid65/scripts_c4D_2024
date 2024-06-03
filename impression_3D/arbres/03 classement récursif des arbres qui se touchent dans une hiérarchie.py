import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

"""sélectionner l'objet contenant les arbres polygonaux'
   Tous les arbres qui se touchent seront sélectionnés
   en partant de celui sélectionné

   Si on veut une marge il faut mettre une distance au BUFFER"""

BUFFER = 0

#TODO -> tenir compte
MAKE_COPY = True

class Arbre(object):

    def __init__(self,obj):
        self.obj = obj
        self.pos = c4d.Vector(obj.GetMg().off)
        self.pos.y = 0
        self.rayon = max(obj.GetRad().x, obj.GetRad().z)* obj.GetAbsScale().x
        self.r2 = self.rayon**2

    def __str__(self):
        return str(self.obj)

    def __lt__(self, other):
        return self.obj.GetName() < other.obj.GetName()

    def __le__(self, other):
        return self.obj.GetName() <= other.obj.GetName()

    def __eq__(self, other):
        return self.obj.GetName() == other.obj.GetName()

    def __ne__(self, other):
        return self.obj.GetName() != other.obj.GetName()

    def __gt__(self, other):
        return self.obj.GetName() > other.obj.GetName()

    def __ge__(self, other):
        return self.obj.GetName() >= other.obj.GetName()


def touch(a1,a2):
    l2 = (a1.pos-a2.pos).GetLength()
    if l2<= a1.rayon+a2.rayon + BUFFER :
        return True


def get_touch(arbre,lst,res ):
    #print('lst ->',len(lst))
    to_remove = []
    for a2 in lst:
        if touch(arbre,a2):
            to_remove.append(a2)
    for a2 in to_remove:
        lst.remove(a2)

    for a2 in to_remove:
        res.append(a2)
        get_touch(a2,lst, res)
    return res



def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    lst_of_lst = []
    lst_isoles = []

    lst = [Arbre(o) for o in op.GetChildren() if o!=op]
    arbre_dprt = lst.pop()
    while arbre_dprt:
        res = [arbre_dprt]
        get_touch(arbre_dprt,lst, res = res)

        #op.DelBit(c4d.BIT_ACTIVE)
        #for a in res:
            #doc.SetActiveObject(a.obj,c4d.SELECTION_ADD)
        if len(res)>1:
            lst_of_lst.append((len(res),res.copy()))
        else:
            lst_isoles.append(res[0])

        res.clear()
        if lst:
            arbre_dprt = lst.pop()
        else:
            arbre_dprt = None
            break
    null_res = c4d.BaseObject(c4d.Onull)
    null_res.SetName(op.GetName()+'_classé')

    #arbres isolés dans un objet neutre
    isoles_neutre = c4d.BaseObject(c4d.Onull)
    isoles_neutre.SetName('isoles')
    for arbre in lst_isoles:
        if MAKE_COPY:
            clone = arbre.obj.GetClone()
            clone.SetMg(c4d.Matrix(arbre.obj.GetMg()))
            clone.InsertUnder(isoles_neutre)
        else:
            arbre.obj.InsertUnder(isoles_neutre)
    isoles_neutre.InsertUnder(null_res)

    #arbres groupes
    grpes_neutre = c4d.BaseObject(c4d.Onull)
    grpes_neutre.SetName('groupes')

    for nb,lst in sorted(lst_of_lst):
        onull = c4d.BaseObject(c4d.Onull)
        onull.SetName(f'{nb} arbres')
        onull.InsertUnder(grpes_neutre)
        for a in lst:
            if MAKE_COPY:
                clone = a.obj.GetClone()
                clone.SetMg(c4d.Matrix(a.obj.GetMg()))
                clone.InsertUnder(onull)
            else:
                a.obj.InsertUnder(onull)
    grpes_neutre.InsertUnder(null_res)
    #print(len(lst_isoles))
    #print(len(lst_of_lst))

    doc.InsertObject(null_res)
    c4d.EventAdd()


if __name__ == '__main__':
    main()