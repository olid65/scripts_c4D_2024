from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

#Pour l'instant manuel modifier les variables fn_gdb et fn_shp 
#au besoin changer aussi ogr
#(un dossier est créé automatiquement m^ême nom que gdb

# coller ensuite le résultat du print dans la console
def main() -> None:
    
    ogr = '/Applications/QGIS.app/Contents/MacOS/bin/ogr2ogr'
    fn_gdb = '/Users/olivierdonze/Downloads/DelatV_projet2024.gdb'
    fn_shp = '/Users/olivierdonze/Downloads/DelatV_projet2024.shp'
    
    #important -lco ENCODING=UTF-8 pour la gestion des caractères dans les champs, sinon on a des erreurs lors de l'importation'
    print(f'{ogr} -f "ESRI Shapefile" {fn_shp} {fn_gdb} -lco ENCODING=UTF-8')

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()