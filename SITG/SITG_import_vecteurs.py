from typing import Optional
import c4d
import requests
import json
import geopandas as gpd

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected


CONTAINER_ORIGIN = 1026473


def empriseObject(obj, origine):
    geom = obj
    if not geom.CheckType(c4d.Opoint):
        geom = geom.GetCache()
        if not geom.CheckType(c4d.Opoint) : return None
    mg = obj.GetMg()
    pts = [p*mg+origine for p in geom.GetAllPoints()]
    lst_x = [p.x for p in pts]
    lst_y = [p.y for p in pts]
    lst_z = [p.z for p in pts]

    xmin = min(lst_x)
    xmax = max(lst_x)
    ymin = min(lst_y)
    ymax = max(lst_y)
    zmin = min(lst_z)
    zmax = max(lst_z)

    mini = c4d.Vector(xmin,ymin,zmin)
    maxi = c4d.Vector(xmax,ymax,zmax)

    return xmin,zmin,xmax,zmax

def main() -> None:
    doc = c4d.documents.GetActiveDocument()
    op = doc.GetActiveObject()
    if not op:
        c4d.gui.MessageDialog("Sélectionnez un objet !")
        return
    origine = doc[CONTAINER_ORIGIN]
    if not origine:
        c4d.gui.MessageDialog("Définissez l'origine !")
        return
    xmin,ymin,xmax,ymax = empriseObject(op, origine)
    width = xmax-xmin
    height = ymax-ymin

    if not width or not height:
        c4d.gui.MessageDialog("L'objet sélectionné n'a pas de surface !")
        return

    layer = 'CAD_OBJETDIVERS_POLY'
    layer = 'CAD_BATIMENT_HORSOL'
    layer = 'CAD_DOMROUTIER_OBJETS_NIV0'
    #layer ='CAD_PARCELLE_MENSU'
    url_base = f'https://vector.sitg.ge.ch/arcgis/rest/services/Hosted/{layer}/FeatureServer/0/query'
    #url_base = 'https://vector.sitg.ge.ch/arcgis/rest/services/Hosted/CAD_OBJETDIVERS_POLY/FeatureServer/0/query'
    url_query = "?f=geojson&where=commune='Meyrin'&outFields=*"
    where = ""#"CODE_OBJET='mur'"
    bbox = f"{xmin},{ymin},{xmax},{ymax}"
    params = {
        'f': 'geojson',
        'outFields': '*',
        'where': where,
        'outSR':2056,
        'inSR':2056,
        'geometry': bbox,
        'geometryType':'esriGeometryEnvelope',
    }
    #url = url_base + url_query
    r = requests.get(url_base, params=params)
    print(r.url)
    data = r.json()
    fn = f'/Users/olivierdonze/Documents/TEMP/SITG_Vector_import/{layer}.geojson'
    with open(fn, "w") as fjson:
        json.dump(data, fjson, indent=4)


"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()