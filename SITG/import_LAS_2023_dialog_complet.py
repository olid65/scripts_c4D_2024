from typing import Optional
import c4d
from pathlib import Path
import zipfile
import urllib

import sys
#print(Path(__file__).parent)
sys.path.append(str(Path(__file__).parent))

import import_LAS_2023_from_bbox_object as LAS

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

CONTAINER_ORIGIN = 1026473

#Dossier pour les téléchargements des tuiles
DIR_DOWNLOAD = Path('/Volumes/My Passport Pro/TEMP/LIDAR_SITG_download')




class ThreadDownload(c4d.threading.C4DThread):

    def __init__(self,lst):
        self.lst = lst
        self.nb_files_to_download = 0
        self.id_file_download = 0


    def show_progress(self,block_num, block_size, total_size):
        downloaded = block_num * block_size
        part = 1/self.nb_files_to_download
        pos = (self.id_file_download-1) * part
        avance = downloaded / total_size*part
        c4d.StatusSetText(f"fichier LIDAR {self.id_file_download} / {self.nb_files_to_download}")
        c4d.StatusSetBar((pos+avance)*100)
        #print(f"Téléchargement en cours... {percent:.2f}%")

    def Main(self):
        #on clacule le nombre de fichier à réellement télécharger pour la status bar
        fn_zips = [Path(str(fn_dst)+'.zip') for url,fn_dst in self.lst if not fn_dst.exists() ]
        self.nb_files_to_download = len(fn_zips)

        self.id_file_download = 0

        for url,fn_dst in self.lst :
            print(fn_dst)
            if fn_dst.exists() : continue
            self.id_file_download +=1
            fn_zip = Path(str(fn_dst)+'.zip')
            if not fn_zip.exists():
                try:
                    urllib.request.urlretrieve(url, fn_zip, reporthook=self.show_progress)
                    #x = urllib.request.urlopen(url)
                    #with open(fn_zip,'wb') as saveFile:
                        #saveFile.write(x.read())


                except Exception as e:
                    print(url)
                    print(str(e))

            if fn_zip.exists():
                #UNZIP
                with zipfile.ZipFile(fn_zip, 'r') as zip_ref:
                    zip_ref.extractall(DIR_DOWNLOAD)

            #on supprime le fichier zip
            if fn_zip.exists() : fn_zip.unlink(missing_ok=True)

        #on remet la status bar à zéro
        c4d.StatusClear()
        self.id_file_download =0
        self.id_file_download = 0


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

    return (mini.x,mini.z, maxi.x,maxi.z)

def get_tiles_within_bounding_box(bounding_box, tile_size=250):
    min_x, min_y, max_x, max_y = bounding_box
    tiles = []

    # Calculer les coordonnées des tuiles touchées
    start_x = (min_x // tile_size) * tile_size
    end_x = (max_x // tile_size) * tile_size
    start_y = (min_y // tile_size) * tile_size
    end_y = (max_y // tile_size) * tile_size

    for x in range(int(start_x), int(end_x) + 1, tile_size):
        for y in range(int(start_y), int(end_y) + 1, tile_size):
            tile_name = f"https://ge.ch/sitg/geodata/SITG/TELECHARGEMENT/LIDAR_2023/{x}_{y}.las.zip"
            #print(tile_name)
            tiles.append(tile_name)

    return tiles


class DlgBbox(c4d.gui.GeDialog):

    ID_BTON_BBOX_OBJECT = 1001
    ID_TXT_NB_LIDAR_TILES = 1002
    ID_BTON_DOWNLOAD = 1010
    ID_CHECKBOX_VEGET_ONLY = 1011

    TXT_NO_LIDAR_TILES = "Aucune tuile"

    MARGIN = 15


    doc = None
    op = None
    bbox = None
    lst_tiles = []
    nb_tiles = None
    veget_only = True

    def CreateLayout(self):

        self.SetTitle("swisstopo extractor")
        # MAIN GROUP
        self.GroupBegin(500, flags=c4d.BFH_CENTER, cols=1, rows=4)
        self.GroupBorderSpace(self.MARGIN*2, self.MARGIN*2, self.MARGIN*2, self.MARGIN*2)

        self.AddButton(self.ID_BTON_BBOX_OBJECT, flags=c4d.BFH_MASK, initw=0, inith=0, name="emprise objet sélectionné")
        self.AddCheckbox(self.ID_CHECKBOX_VEGET_ONLY, flags=c4d.BFH_CENTER,  initw=200, inith=30, name="Végétation seulement")
        self.AddStaticText(self.ID_TXT_NB_LIDAR_TILES, flags=c4d.BFH_CENTER, initw=200, inith=30, name=self.TXT_NO_LIDAR_TILES, borderstyle=c4d.BORDER_WITH_TITLE_BOLD)
        self.AddButton(self.ID_BTON_DOWNLOAD, flags=c4d.BFH_MASK, initw=0, inith=0, name="télécharger les lidar")

        self.GroupEnd()
        return True

    def InitValues(self):
        self.maj_bbox()
        if self.bbox:
            self.SetString(self.ID_TXT_NB_LIDAR_TILES,f"Il y a {self.nb_tiles} tuiles à télécharger")
        self.SetBool(self.ID_CHECKBOX_VEGET_ONLY,True)
        self.veget_only = True
        return True

    def maj_bbox(self):
        self.bbox = None
        self.lst_tiles = []
        self.nb_tiles = 0
        self.doc = c4d.documents.GetActiveDocument()
        self.origin = self.doc[CONTAINER_ORIGIN]
        if not self.origin:
            print("pas d'origine")
            self.bbox = None

        #TODO -> dlg -> si on n'a pas d'origine
        self.op = self.doc.GetActiveObject()
        if self.op:
            self.bbox = empriseObject(self.op, self.origin)
            self.lst_tiles = get_tiles_within_bounding_box(self.bbox, tile_size=250)
            self.nb_tiles = len(self.lst_tiles)

    def Command(self, id, msg):
        if id == self.ID_BTON_BBOX_OBJECT:
            self.maj_bbox()
            if self.bbox:
                self.SetString(self.ID_TXT_NB_LIDAR_TILES,f"Il y a {self.nb_tiles} tuiles à télécharger")
                
        if id == self.ID_CHECKBOX_VEGET_ONLY:
            self.veget_only = self.GetBool(self.ID_CHECKBOX_VEGET_ONLY)

        ############DOWNLOAD ##############################################
        if id ==self.ID_BTON_DOWNLOAD:

            if not DIR_DOWNLOAD.is_dir():
                print("Le dossier de téléchargement n'existe pas")
                return True
            #list de tuple url,fn_dest pour envoyer dans le Thread
            self.dwload_lst = []

            for url in self.lst_tiles:
                name_file = DIR_DOWNLOAD / Path(url.split('/')[-1][:-4])
                self.dwload_lst.append((url,name_file))

            if self.dwload_lst :
                #LANCEMENT DU THREAD
                self.thread = ThreadDownload(self.dwload_lst)
                self.thread.Start()
                self.SetTimer(500)
                #variable pour eviter de lancer la génération de la maquette plusieurs fois
                self.gen = True

        return True


    def Timer(self,msg):
        #print('timer')
        #si le thread est terminé on arrête le Timer et on lance la création des vrt
        if not self.thread.IsRunning():
            print('terminé')
            self.SetTimer(0)
            if self.gen :
                self.gen = False
                if c4d.gui.QuestionDialog("Téléchargement terminé, voulez-vous importer les LIDAR"):
                    list_fn = [fn for url,fn in self.dwload_lst]
                    LAS.extractLAS(list_fn, self.bbox,self.doc,veget_only=self.veget_only)


def main() -> None:
    # Called when the plugin is selected by the user. Similar to CommandData.Execute.
    c4d.gui.MessageDialog("Hello World!")

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    #main()
    dlg = DlgBbox()
    dlg.Open(c4d.DLG_TYPE_ASYNC)