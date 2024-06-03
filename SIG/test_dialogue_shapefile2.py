import c4d, os, shapefile


BORDER_SPACE = 5

ID_FN_TXT  = 1001
ID_FN      = 1002
ID_FN_BTON = 1003

ID_LIST_CHAMP_TXT    = 1011
ID_LIST_CHAMP        = 1012

class MonDlg(c4d.gui.GeDialog):
    def __init__(self,fn = None):
        self.fn = fn
        self.grouper = False
        self.fields = ['__aucun__']
        self.choix_champ = 0
    
    def CreateLayout(self):
        self.SetTitle('Importer un fichier shape : ')
        self.GroupBegin(1000,flags=c4d.BFH_SCALEFIT, cols=3, rows=1)
        self.GroupBorderSpace(BORDER_SPACE*2, BORDER_SPACE*2, BORDER_SPACE*2, int(BORDER_SPACE/2))
        self.AddStaticText(ID_FN_TXT,name="Fichier shape :", flags=c4d.BFH_MASK,initw=110)
        self.AddEditText(ID_FN, flags=c4d.BFH_MASK,initw=500)
        self.AddButton(ID_FN_BTON,flags=c4d.BFH_MASK,initw=20, name ='...')
        self.GroupEnd()

        #LISTE DES CHAMPS ()
        self.GroupBegin(1010,flags=c4d.BFH_SCALEFIT, cols=2, rows=1)
        self.GroupBorderSpace(BORDER_SPACE*2, BORDER_SPACE*2, BORDER_SPACE*2, int(BORDER_SPACE/2))
        self.AddStaticText(ID_LIST_CHAMP_TXT,name="Grouper par la valeur d'un champ : ", flags=c4d.BFH_MASK,
                                             initw=280)
                                            
        self.AddComboBox(ID_LIST_CHAMP,flags=c4d.BFH_MASK, initw=200) 
        self.GroupEnd()
            
        self.AddDlgGroup(c4d.DLG_OK|c4d.DLG_CANCEL)    
        return True
    
    def InitValues(self):
        if self.fn :
            self.SetString(ID_FN,self.fn)
            
        self.FreeChildren(ID_LIST_CHAMP)    
        for i,n in enumerate(self.fields):
            self.AddChild(ID_LIST_CHAMP,i,n)
        self.SetLong(ID_LIST_CHAMP,self.choix_champ)
                
            
        return True
    
    def maj_fields(self):
        """renvoie une liste des noms de champ de self.fn"""
        del(self.fields[:])
        self.fields = ['__aucun__']
        if self.fn :
            shp = shapefile.Reader(self.fn)
            self.fields += [f[0] for f in shp.fields[1:]]
            print (self.fields)
        
    def maj(self):
        """met à jour la boîte de dialogue"""
        self.maj_fields()
        self.CreateLayout()
        self.InitValues()
        print ('maj')
    
    
    def Command(self,id,msg): 
        if id == c4d.DLG_OK:
            self.Close()
            
        elif id == c4d.DLG_CANCEL:
            self.Close()
            
        elif id==ID_FN_BTON : 
            fn = c4d.storage.LoadDialog()
            if fn :
                #on recherche les fichier shape si c'est par ex le dbf qui a été choisi
                path,ext = os.path.splitext(fn)
                fn = path + '.shp'
                #vérification que le fichier existe
                if not os.path.isfile(fn):
                    c4d.gui.MessageDialog("ce n'est pas un fichier shape valide")
                    self.SetString(ID_FN, '')
                
                else :
                    self.fn = fn
                    self.SetString(ID_FN, self.fn)
                    self.maj()
        
        elif id == ID_FN:
            self.maj()
            
        
            
        return True

def main():
    dlg = MonDlg()
    dlg.Open(c4d.DLG_TYPE_MODAL)

if __name__=='__main__':
    main()
