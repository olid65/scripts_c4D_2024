import c4d,json
import webbrowser




ID_LIST_LYR_TXT = 1003
ID_LIST_LYR = 1004

ID_FILTRE_TXT = 1005
ID_FILTRE = 1006

ID_INFO_BTON = 1007


BORDER_SPACE = 10

class MonDlg(c4d.gui.GeDialog):
    def __init__(self, lst_lyr):
        self.layers = lst_lyr
        self.lyrs_filtred = list(self.layers)
        self.cancel = False
        self.id_lyr = 0

    def CreateLayout(self):
        self.SetTitle('Extraction vecteur SITG : ')
        self.GroupBegin(1000,flags=c4d.BFH_SCALEFIT, cols=2, rows=2)
        self.GroupBorderSpace(BORDER_SPACE*2, BORDER_SPACE*2, BORDER_SPACE*2, int(BORDER_SPACE/2))
        self.AddStaticText(ID_FILTRE_TXT,name="Filtre : ", flags=c4d.BFH_MASK,
                                             initw=200)
        self.AddEditText(ID_FILTRE,flags=c4d.BFH_MASK, initw=200)
        self.AddStaticText(ID_LIST_LYR_TXT,name="Couche : ", flags=c4d.BFH_MASK,
                                             initw=200)
                                            
        self.AddComboBox(ID_LIST_LYR,flags=c4d.BFH_MASK, initw=200) 
        self.GroupEnd()
        
        self.GroupBegin(1001,flags=c4d.BFH_CENTER, cols=1, rows=1)
        self.GroupBorderSpace(BORDER_SPACE*2, 0, BORDER_SPACE*2, 0)
        self.AddButton(ID_INFO_BTON, flags=c4d.BFH_MASK,initw=150,inith = 15, name = 'info')
        
        self.GroupEnd()
        
        self.GroupBegin(1002,flags=c4d.BFH_CENTER, cols=2, rows=1)
        self.GroupBorderSpace(BORDER_SPACE*2, 0, BORDER_SPACE*2, 0)
        
        self.AddDlgGroup(c4d.DLG_OK|c4d.DLG_CANCEL)
        
        self.GroupEnd()
        return True
        
    def InitValues(self):
        for name,i in self.lyrs_filtred:
            self.AddChild(ID_LIST_LYR,i,name)
        
        return True
    
    def majCombo(self):
        self.FreeChildren(ID_LIST_LYR)
        for name,i in self.lyrs_filtred:
            self.AddChild(ID_LIST_LYR,i,name)
        
    def Command(self,id,msg): 
        
        if id==ID_LIST_LYR :
            self.id_lyr = self.GetLong(ID_LIST_LYR)
            print (self.id_lyr)
            
        if id == ID_FILTRE:
            txt = self.GetString(ID_FILTRE).upper()
            self.lyrs_filtred = [(name,i) for name,i in self.layers if txt in name]
            self.majCombo()  

        if id == ID_INFO_BTON:
            webbrowser.open('http://www.tdg.ch/')
            
            
        if id == c4d.DLG_OK:
            self.Close()
            
        
        if id == c4d.DLG_CANCEL:
            self.Close()
            self.cancel = True
            
        return True

def main():
    global dlg
    fn ='/Users/olivierdonze/switchdrive/C4D_scripts_et_plugins/OLD_scripts/scripts_maison/SCRIPTS_PLUGINS_PAR_VERSION_C4D_seau_champagne/R17/scripts/SITG/SITG_OPENDATA_VECTOR_STRUCTURE_JSON/LAYERS.json'
    lst_lyr = []
    with open(fn) as f:
        data = json.load(f)
        
        for lyr in data['layers']:
            lst_lyr.append((lyr['name'],lyr['id']))
    lst_lyr.sort()
    dlg = MonDlg(lst_lyr)
    dlg.Open(c4d.DLG_TYPE_ASYNC)
    if dlg.cancel : return

if __name__=='__main__':
    main()
