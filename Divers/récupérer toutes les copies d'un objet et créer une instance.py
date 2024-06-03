import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def getAllChairs(obj,name = 'Prop_Chair_01',res = []):

    while obj:

        if obj.CheckType(c4d.Opolygon) and obj.GetName()==name:
            res.append(obj)
        getAllChairs(obj.GetCache(),name,res)
        getAllChairs(obj.GetDown(),name,res)
        obj = obj.GetNext()
    return res

def roundVec(v,nb = 0):
    return c4d.Vector(round(v.x,nb),round(v.y,nb),round(v.z,nb))

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    res = c4d.BaseObject(c4d.Onull)
    obj = op.GetDown()
    lst = getAllChairs(obj,name = 'Prop_Chair_01')
    print(len(lst))
    positions = []
    i = 1
    for o in lst:
        pos = roundVec(o.GetMg().off)
        if not pos in positions:
            i+=1
            positions.append(pos)
            inst = c4d.BaseObject(c4d.Oinstance)
            inst.SetMg(c4d.Matrix(o.GetMg()))
            inst.InsertUnderLast(res)
    print(i)

    doc.InsertObject(res)
    c4d.EventAdd()

if __name__ == '__main__':
    main()