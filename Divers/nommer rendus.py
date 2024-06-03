from typing import Optional
import c4d
import os

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

NOM_DOSSIER_RENDU = "rendus"

def main() -> None:
    if not doc.GetDocumentPath():
        c4d.gui.MessageDialog("Le document doit d'abord être enregistré")
        return
    name = doc.GetDocumentName()[:-4]
    path = os.path.join(doc.GetDocumentPath(),NOM_DOSSIER_RENDU,name + "$camera_$YY_$MM_$DD_$hh_$mm")
   
    rd = doc.GetActiveRenderData()
    rd[c4d.RDATA_PATH] = path
    c4d.EventAdd()
   
    #$camera_$YY_$MM_$DD_$hh_$mm

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
