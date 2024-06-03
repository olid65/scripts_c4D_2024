import c4d
import os.path
import subprocess
import sys


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

#-p pour générer de polygones
#-i -> intervalle
#-3D pour poly 3D

#Attention le GeoJson ne s'affiche pas dans Qgis !?
DIC_FORMATS = {
                'GeoJSON':'.geojson',
                'ESRI Shapefile':'.shp',
                'DXF':'.dxf',
                }

TXT_NO_PATH_TO_QGIS = "QGis ne semble pas installé sur cette machine, opération impossible !"

def getPathToQGISbin(path_to_QGIS = None):
    #Si le path_to_QGIS n'est pas renseigné on prend le chemin par défaut selon la plateforme
    win = sys.platform == 'win32'
    if not path_to_QGIS:
        if sys.platform == 'win32':
            path_to_QGIS = 'C:\\Program Files'
        else:
            path_to_QGIS = '/Applications'
    for folder_name in os.listdir(path_to_QGIS):
        if 'QGIS'  in folder_name:
            if win :
                path = os.path.join(path_to_QGIS,folder_name,'bin')
            else:

                path = os.path.join(path_to_QGIS,folder_name,'Contents/MacOS/bin')

            if os.path.isdir(path):
                return path
    return None

def gdalBIN_OK(path_to_QGIS_bin, exe = 'gdal_translate'):
    if sys.platform == 'win32':
        exe+='.exe'
    path = os.path.join(path_to_QGIS_bin,exe)
    if os.path.isfile(path):
        return path
    else:
        return False


def ogr2ogr(infile,outfile, simplify_tolerance = None):
    """l'extension sert à définir le format"""
    #ogr2ogr -f DXF "E:\OD\TEMP\test_courbes\Landscape_courbes_1m.dxf" "E:\OD\TEMP\test_courbes\Landscape_courbes_1m.geojson"
    #ogr2ogr -f GeoJSON -t_srs EPSG:5070 [outFile.geojson] [inFile.shp] 
    qgispath = getPathToQGISbin()
    if not qgispath:
        c4d.gui.MessageDialog(TXT_NO_PATH_TO_QGIS)
        return False
    pth_ogr2ogr = os.path.join(qgispath,'ogr2ogr')
    if not os.path.isfile(pth_ogr2ogr) and not os.path.isfile(pth_ogr2ogr+'.exe'):
        c4d.gui.MessageDialog(f"Pas de fichier ogr2ogr : {pth_ogr2ogr}")
        return False
    simpl = ''
    if simplify_tolerance:
        simpl = f'-simplify {simplify_tolerance}'

    req = f'''"{pth_ogr2ogr}" -a_srs EPSG:2056 {simpl} "{outfile}" "{infile}" '''
    #print(req)
    output = subprocess.check_output(req,shell=True)



def gdal_contour(fn_mnt,polygon = True, fn_curves = None, equidist=1, geom3D =True, form = 'GeoJSON'):
    qgispath = getPathToQGISbin()
    if not qgispath:
        c4d.gui.MessageDialog(TXT_NO_PATH_TO_QGIS)
        return False
    pth_gdal_contour = os.path.join(qgispath,'gdal_contour')
    if not os.path.isfile(pth_gdal_contour) and not os.path.isfile(pth_gdal_contour+'.exe'):
        c4d.gui.MessageDialog(f"Pas de fichier gdal_contour : {pth_gdal_contour}")
        return False
    #si le fichier de det n'est pas renseigné on fait un nom automatique
    if not fn_curves:
        name,ext = os.path.splitext(fn_mnt)
        poly = ''
        if polygon:
            poly='_poly'
        fn_curves = name + f'_courbes{poly}_{equidist}m' + DIC_FORMATS[form]

    if geom3D:
        g3D = '-3d'
    else:
        g3D = ''

    if polygon:
        p = '-p'
    else:
        p = ''


    req = f'''"{pth_gdal_contour}" {p} -amax ELEV_MAX -amin ELEV_MIN -b 1 -i {equidist} {g3D} -f "{form}" {fn_mnt} {fn_curves}'''
    #print(req)
    output = subprocess.check_output(req,shell=True)

# Main function
def main():
    fn_mnt = '/Users/olivierdonze/Documents/TEMP/Martigny_Combe/mnt_esri_test.asc'

    gdal_contour(fn_mnt,fn_curves = None, equidist=5, geom3D =True)

# Execute main()
if __name__=='__main__':
    main()