from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

CONNECTOR_TOLERANCE = 0.001

VOXEL_SIZE = 0.5

VOL_MESHER_ADAPTATIVE = 0.1

SUFFIXE_NAME = 'volume'

#True si on veut directement obtenir un objet polygonal
CONVERTIR = True


def main() -> None:
    #cloner l'objet et la hiérarchie
    clone = op.GetClone(flags=c4d.COPYFLAGS_NONE)
   
    #mettre dans un connecteur
    connector = c4d.BaseObject(c4d.Oconnector)
    connector[c4d.CONNECTOBJECT_TOLERANCE]=CONNECTOR_TOLERANCE
    connector[c4d.CONNECTOBJECT_PHONG_MODE] =c4d.CONNECTOBJECT_PHONG_MODE_LOW
    clone.InsertUnder(connector)
    #mettre dans un générateur de volume Ovolume
    #gen_vol = c4d.BaseObject(c4d.Ovolume)
    gen_vol = c4d.modules.volume.VolumeBuilder()
    gen_vol[c4d.ID_VOLUMEBUILDER_GRID_SIZE] = VOXEL_SIZE
    connector.InsertUnder(gen_vol)
    gen_vol.AddSceneObject(connector)
    #metrre dans un mailleur de volume
    vol_mesher = c4d.BaseObject(c4d.Ovolumemesher)
    gen_vol.InsertUnder(vol_mesher)
    vol_mesher[c4d.ID_VOLUMETOMESH_ADAPTIVE_VALUE] = VOL_MESHER_ADAPTATIVE
    doc.InsertObject(vol_mesher)
   
    #rendre actif le mailleur
    doc.SetActiveObject(vol_mesher)
   
    #désactiver l'objet d'origine dans la vue et au rendu
    op[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = c4d.OBJECT_OFF
    op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = c4d.OBJECT_OFF
   
    #convertir en objet
    if CONVERTIR:
        #MCOMMAND_MAKEEDITABLE
        res = c4d.utils.SendModelingCommand(c4d.MCOMMAND_MAKEEDITABLE, [vol_mesher])
        if res:
            obj = res[0]
            #suppression des enfants
            child = obj.GetDown()
            while child:
                child.Remove()
                child = obj.GetDown()
            doc.InsertObject(obj)
            obj.SetName(f'{op.GetName()}_{SUFFIXE_NAME}')

    c4d.EventAdd()

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()

