
import c4d
import os

# localimport-v1.7.3-blob-mcw79
import base64 as b, types as t, zlib as z; m=t.ModuleType('localimport');
m.__file__ = __file__; blob=b'\
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\
XVw='
exec(z.decompress(b.b64decode(blob)), vars(m)); _localimport=m;localimport=getattr(m,"localimport")
del blob, b, t, z, m;

# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

CONTAINER_ORIGIN = 1026473

TXT_NO_SELECTION = "Il n'y a pas de terrain sélectionné opération impossible"

TXT_NOT_SAVED = "Le document doit être enregistré pour pouvoir générer différents fichiers, vous pourrez le faire à la prochaine étape\nVoulez-vous continuer ?"
TXT_DOC_NOT_IN_METERS = "Les unités du document ne sont pas en mètres, si vous continuez les unités seront modifiées.\nVoulez-vous continuer ?"
TXT_NAS_HEPIA = "Votre document est enregistré sur le NAS (hes-nas-prairie.hes.adhes.hesge.ch).\nEnregistrez le projet et les ressources utilisées sur un autre disque (disque dur externe, Partage, ou dossier à votre nom à la racine de C:)"
TXT_PATH_CAR_SPECIAL = "Le chemin de fichier continet un ou plusieurs caractères spéciaux (accents,cédille,...) \nImport impossible !"

class DlgContoursMNT(c4d.gui.GeDialog):

    MARGIN = 5

    ID_TXT_EQUIDIST = 1000
    ID_EQUIDIST = 1001
    ID_NB_CONTOUR = 1003


    ID_CBOX_POLYGON = 1010
    ID_CBOX_3D = 1011
    ID_CBOX_DXF =1012

    ID_BTON_GENERATE_CONTOUR = 1020


    TXT_EQUIDIST = 'Equidiatance des courbes :'
    LABEL_CBOX_POLYGON = 'Générer des polygones fermés'
    LABEL_CBOX_3D = 'Courbes 3D'
    LABEL_CBOX_DXF = 'Exporter un fichier dxf'

    LABEL_GENERATE_CONTOUR = 'Générer les courbes de niveau'




    def __init__(self,mnt, doc):
        self.mnt = mnt
        self.doc = doc

    def CreateLayout(self):
        self.SetTitle("Courbes de niveau depuis terrain")
        # MAIN GROUP
        self.GroupBegin(500, flags=c4d.BFH_CENTER, cols=1, rows=6)
        self.GroupBorderSpace(self.MARGIN*2, self.MARGIN*2, self.MARGIN*2, self.MARGIN*2)

        #Equidistance
        self.AddStaticText(self.ID_TXT_EQUIDIST, name=self.TXT_EQUIDIST, flags=c4d.BFH_MASK, initw=200)
        self.AddEditSlider(self.ID_EQUIDIST, flags=c4d.BFH_MASK, initw=50, inith=20)
        self.AddStaticText(self.ID_NB_CONTOUR,flags=c4d.BFH_MASK, initw=50, inith=20, name='Nombre de courbes', borderstyle=0)

        #polygone fermé
        self.AddCheckbox(self.ID_CBOX_POLYGON, flags=c4d.BFH_MASK, initw=300, inith=20, name = self.LABEL_CBOX_POLYGON)
        #3D
        self.AddCheckbox(self.ID_CBOX_3D, flags=c4d.BFH_MASK, initw=300, inith=20, name = self.LABEL_CBOX_3D)

        #DXF
        self.AddCheckbox(self.ID_CBOX_DXF, flags=c4d.BFH_MASK, initw=300, inith=20, name = self.LABEL_CBOX_DXF)

        #bouton
        self.AddButton(self.ID_BTON_GENERATE_CONTOUR, flags=c4d.BFH_MASK, initw=300, inith=30, name=self.LABEL_GENERATE_CONTOUR)

        #END MAIN GROUP
        self.GroupEnd()

        return True

    def InitValues(self):

        self.SetFloat(self.ID_EQUIDIST,1.0,min=0.1, max=100, step=1.0, format=c4d.FORMAT_METER, min2=0.1, max2=100.0, quadscale=True, tristate=False)
        #self.SetMeter(self.ID_EQUIDIST, 1.0)
        self.SetBool(self.ID_CBOX_POLYGON,False)
        self.SetBool(self.ID_CBOX_3D,True)
        self.SetBool(self.ID_CBOX_DXF,True)

        self.maj_nb_courbes()

        return True

    def maj_nb_courbes(self):
        nb_courbes = int(round(self.mnt.GetRad().y *2/ self.GetFloat(self.ID_EQUIDIST)))
        self.SetString(self.ID_NB_CONTOUR, f'soit env. {nb_courbes} courbes')


    def Command(self, id, msg):
        if id== self.ID_EQUIDIST:
            self.maj_nb_courbes()
        # Choix du lieu
        if id == self.ID_BTON_GENERATE_CONTOUR:
            path_doc = doc.GetDocumentPath()

            while not path_doc:
                rep = c4d.gui.QuestionDialog(TXT_NOT_SAVED)
                if not rep : return True
                c4d.documents.SaveDocument(doc, "", c4d.SAVEDOCUMENTFLAGS_DIALOGSALLOWED, c4d.FORMAT_C4DEXPORT)
                c4d.CallCommand(12098) # Enregistrer le projet
                path_doc = doc.GetDocumentPath()

            #Vérification qu'on n'est pas sur le NAS de l'école
            if 'hes-nas-prairie.hes.adhes.hesge.ch' in path_doc:
                c4d.gui.MessageDialog(TXT_NAS_HEPIA)
                return True

            #Vérification qu'il n'y ait pas de caractères spéciaux dans le chemin !
            #GDAL ne supporte pas
            try :
                path_doc.encode(encoding='ASCII')
            except:
                c4d.gui.MessageDialog(TXT_PATH_CAR_SPECIAL)
                return True

            with localimport(os.path.dirname(__file__)) as importer:

                #EXPORT DU MNT EN ASCII
                importer.disable(['export_mnt'])
                from od_lib_temp import export_mnt
                fn_mnt = os.path.join(path_doc,f'{self.mnt.GetName()}.asc')
                origin = self.doc[CONTAINER_ORIGIN]

                #si on n'a pas d'origin on met à zéro, pour une utilisation hors doc géoréf
                if not origin :
                    origin = c4d.Vector(0)
                    self.doc[CONTAINER_ORIGIN] = origin
                export_mnt.export_mnt_ascii(self.mnt,fn_mnt,origin)

                #EXTRACTION DES COURBES
                importer.disable(['gdal_c4d'])
                from od_lib_temp import gdal_c4d

                equidist = self.GetFloat(self.ID_EQUIDIST)
                geom3D = self.GetBool(self.ID_CBOX_3D)
                polygon = self.GetBool(self.ID_CBOX_POLYGON)

                #si on a un chiffre à virgule on met la taille en cm dans le nom du fichier, sinon en m
                if round(equidist*100)%100:
                    txt_equidist = f'{round(equidist*100)}cm'
                else:
                    txt_equidist = f'{round(equidist)}m'

                #TODO attention au nom gdal est très sensible !
                fn_curves = os.path.join(path_doc,f'{self.mnt.GetName()}_courbes_{txt_equidist}.geojson')
                gdal_c4d.gdal_contour(fn_mnt,polygon = polygon, fn_curves = fn_curves, equidist=equidist, geom3D =geom3D, form = 'GeoJSON')

                importer.disable(['geojson2spline'])
                from od_lib_temp import geojson2spline
                geojson2spline.main(fn_curves,doc)

                #DXF
                if self.GetBool(self.ID_CBOX_DXF):
                    try:
                        outfile = fn_curves.replace('.geojson','.dxf')
                        gdal_c4d.ogr2ogr(fn_curves,outfile)
                    except:
                        c4d.gui.MessageDialog("Problème lors de la génération du DXF")

                #TEST SIMPLIFICATION DES COURBES
                #ATTENTION J'AI REUSSI A LE FAIRE FONCTIONNER SEULEMENT A PARTIR D?UN SHAPE (ne fonctionne pas avec geojson !!!)
                # fact_simpl = 5
                # fn_shp = fn_curves.replace('.geojson','.shp')
                # gdal_c4d.gdal_contour(fn_mnt,polygon = polygon, fn_curves = fn_shp, equidist=equidist, geom3D =geom3D, form = 'ESRI shapefile')
                # fn_curves_simpl = fn_curves[:-len('.geojson')]+f'_simpl_{fact_simpl}.shp'
                # gdal_c4d.ogr2ogr(fn_shp,fn_curves_simpl,fact_simpl)



            self.Close()



        return True


# Main function
def main():

    doc = c4d.documents.GetActiveDocument()

    #Vérification objet sélectionné, objet polygonal, grille régulière
    #TODO -> créer un plugin objet pour les terrains, avec lien sur le fichier d'origine
    mnt = doc.GetActiveObject()

    if not mnt:
        c4d.gui.MessageDialog(TXT_NO_SELECTION)
        return False

    if not mnt.CheckType(c4d.Opolygon):
        c4d.gui.MessageDialog(f"{mnt.GetName()} n'est pas un objet polygonal")
        return False

    dlg = DlgContoursMNT(mnt,doc)
    dlg.Open(c4d.DLG_TYPE_MODAL)
    c4d.EventAdd()

    #DIALOGUE
    #polygone ou polylignes
    #3D/2D
    #choix de l'équidistance
    #export dxf, shape, geojson ?
    #chemin et nom du fichier d'export
    #importer les courbes ?
    ###splines (et étiquettes altitudes?)
    ###terrain terrasses
    ###terrain terrassse imprimable (mailleur)
    #générer une texture et la plaquer sur le terrain ?




    #exportation du mnt en asci
    #éventuellement simplifier le mnt ? -> pour faire un premier lissage

    #génération des courbes avec gdal_contour

    #importation des courbes dans c4d

    #ou terrain escaliers
    #ou terrain escaliers imprimable
    #générer un raster avec les courbes pour plaquer sur le terrain
    #exporter les courbes en dxf (ou autre)






# Execute main()
if __name__=='__main__':
    main()