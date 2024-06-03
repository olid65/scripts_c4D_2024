import c4d
from pprint import pprint

import os,glob,shutil

import sys

sys.path.append('/Users/olivierdonze/opt/anaconda3/lib/python3.8/site-packages')

import xlrd


NOM_LISTE_ETUDIANTS = 'etudiants.xls'
NOM_IMG_BASES = 'images_base'
NOM_DIR_CIBLE = 'donnees_etudiants'
NOM_DIR_RENDU = 'dossiers_rendu'
   
def watermark(fn_srce,fn_cible,txt,taille_font=100,posx = 500,posy =500):
    gcm = c4d.bitmaps.GeClipMap()
    gcm.InitWith(fn_srce,0)
    gcm.BeginDraw()
    gcm.SetDrawMode(c4d.GE_CM_BLIT_COL, 100)
    bc = c4d.BaseContainer()
    gcm.SetFont(bc, taille_font)
    gcm.TextAt(posx, posy, txt)
    gcm.EndDraw()
    bmp = gcm.GetBitmap()
    bmp.Save(fn_cible,c4d.FILTER_JPG)
    #c4d.bitmaps.ShowBitmap(bmp)
    
#FN_IMG = '/Users/donzeo/Documents/TEMP/test_watermark/maquette_complete.tif'

def main():
    #path = c4d.storage.LoadDialog(title= "sélectionner le dossier",flags = c4d.FILESELECT_DIRECTORY)
    path = '/Users/olivierdonze/switchdrive/COURS/ORG_GN_2021/examens/exa1_2019'
    if not path: return
    dir_cible = os.path.join(path,NOM_DIR_CIBLE)
    if not os.path.isdir(dir_cible):
        os.mkdir(dir_cible)
        
    dir_rendu = os.path.join(path,NOM_DIR_RENDU)
    if not os.path.isdir(dir_rendu):
        os.mkdir(dir_rendu)
    
    fn_xls=dn=None
    for fn in os.listdir(path):
        if fn == NOM_LISTE_ETUDIANTS:
            fn_xls = os.path.join(path,fn)
        elif fn == NOM_IMG_BASES:
            dn = os.path.join(path,fn)
            
    if not fn_xls :
        print ('pas de fichier Excel')
        return
    if not dn:
        print ('pas de dossier images')
        return

    #liste des images à watermarker
    lst_img = [fn for fn in glob.glob(os.path.join(dn,'*.jpg'))]
    #liste des autres fichiers à copier
    fn2copy = [fn for fn in glob.glob(os.path.join(dn,'*')) if fn not in lst_img]

    wb = xlrd.open_workbook(fn_xls)
    sht =  wb.sheets()[0]
    
    for rownum in range(sht.nrows):
        nom = sht.row_values(rownum)[0]
        dn = os.path.join(dir_cible,nom)
        #print(dn)
        #le chemin en unicode posait problème à c4d.Bitmaps mais pas pou rla creation des dossiers
        #dn = dn.encode('utf-8')
        #creation des dossiers donnees
        if not os.path.isdir(dn):
            os.makedirs(dn) 
            
        #création des dossier rendu
        dossiers_rendu = os.path.join(dir_rendu,nom)
        if not os.path.isdir(dossiers_rendu):
            os.makedirs(dossiers_rendu)
        
        #RECUPERATION DES INITIALES (PAS UTILISES POUR L'INSTANT)
        initiales = u''
        for txt in nom.split():
            for t in txt.split('-'):
                initiales+=t[0]
        
        #creation de l'image avec le watermark (voir fonction)
        for fn_img in lst_img :
            bmp = c4d.bitmaps.BaseBitmap()
            bmp.InitWith(fn_img)
            x,y = bmp.GetSize()
            nom_img = os.path.basename(fn_img)
            taille_car = 80
            #if nom_img == 'ortho_PAV.jpg' : taille_car *=4
            nb_car = len(nom)
            pos_x = int(x/2.0 - nb_car*taille_car/2.0)
            if pos_x<0 : pos_x =0
            #print(dn,nom_img)
            watermark(fn_img,os.path.join(dn,nom_img),nom,taille_font=taille_car,posx = pos_x,posy =y/2-taille_car) 
      
        #copie des autres fichiers
        for fn_copy in fn2copy:
            shutil.copy(fn_copy,dn)
    
if __name__=='__main__':
    main()
