from typing import Optional
import c4d
from random import choice

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected



def modify_instance(obj, lst):
    while obj:
        if obj.CheckType(c4d.Oinstance):
            doc.AddUndo(c4d.UNDOTYPE_CHANGE,obj)
            obj[c4d.INSTANCEOBJECT_LINK] = choice(lst)
        modify_instance(obj.GetDown(), lst)
        obj = obj.GetNext()

def modify_cloner_children(obj, lst):
    while obj:
        #si cloner
        if obj.CheckType(1018544):
            #print(obj.GetName())
            for o in obj.GetChildren():
                doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ,o)
                o.Remove()
            for o in lst:
                clone = o.GetClone()
                clone.InsertUnderLast(obj)
                doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,o)

        modify_cloner_children(obj.GetDown(), lst)
        obj = obj.GetNext()

def main() -> None:
    nom_remplace = '__remplacement'
    null_remplace = doc.SearchObject(nom_remplace)
    if not null_remplace:
        print(f"""pas d'objet nommé"{nom_remplace}" """)
    objs = null_remplace.GetChildren()
    doc.StartUndo()
    modify_instance(doc.GetFirstObject(), objs)
    modify_cloner_children(doc.GetFirstObject(), objs)
    doc.EndUndo()
    c4d.EventAdd()


def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED


if __name__ == '__main__':
    main()