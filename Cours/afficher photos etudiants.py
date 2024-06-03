import c4d,os
from c4d import gui,bitmaps
from glob import glob
from random import shuffle


MY_BITMAP_BUTTON = 10000

#Liste de tuple nom/chemin des chemins possible

DOSSIERS = [("Illustrator/Photoshop 2 2017 groupe 1", '/Users/donzeo/Documents/Cours/Illustrator Photoshop 2 automne 2017/photos/Cours1'),
            ("Illustrator/Photoshop 2 2017 groupe 2", '/Users/donzeo/Documents/Cours/Illustrator Photoshop 2 automne 2017/photos/Cours2'),
            ("Cinema 4D niv1 automne 2017",           '/Users/donzeo/Documents/Cours/Cinema4D_niv1_automne2017/photos')]

class MyDialog(c4d.gui.GeDialog):

    def __init__(self,lst_fn):
        self.lst_fn = lst_fn
        self.cnt = len(self.lst_fn)
        self.lst_rdm = self.lst_fn[:]
        shuffle(self.lst_rdm)
        self.fn = self.lst_rdm.pop()
        self.change = False
        self.name = None

    def CreateLayout(self):

        self.SetTitle("My Python Dialog")

        self.GroupBegin(0, c4d.BFH_SCALEFIT|c4d.BFH_SCALEFIT, 1, self.cnt, "Bitmap Example",0)

        bc = c4d.BaseContainer()                            #Create a new container to store the button image
        fn = c4d.storage.GeGetC4DPath(c4d.C4D_PATH_DESKTOP) #Gets the desktop path
        #path = '/Volumes/SITG_OD/Obliques_2013/E_thumbnails/260020024_1.jpg' #os.path.join(fn,'myimage.jpg')               #The path to the image
        bc.SetFilename(MY_BITMAP_BUTTON, self.fn)              #Add this location info to the conatiner
        self.myBitButton=self.AddCustomGui(MY_BITMAP_BUTTON, c4d.CUSTOMGUI_BITMAPBUTTON, "Bitmap Button", c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 30, 30, bc)
        self.myBitButton.SetImage(self.fn, False)             #Add the image to the button
        self.name,ext = os.path.splitext(os.path.basename(self.fn))
        self.GroupEnd()
        return True

    def maj(self):
        self.myBitButton.SetImage(self.fn, False)


    #Do something when the button is pressed
    def Command(self, id, msg=None):
        if id>=MY_BITMAP_BUTTON:
            if self.change:
                #self.name,ext = os.path.splitext(os.path.basename(self.fn))
                #print (name)
                if not (len(self.lst_rdm)):
                   self.lst_rdm = self.lst_fn[:]
                   shuffle(self.lst_rdm)

                self.fn = self.lst_rdm.pop()
                self.name,ext = os.path.splitext(os.path.basename(self.fn))
                self.maj()
                self.change = False
            else:
                print (self.name)
                self.change = True

        return True






if __name__=='__main__':

    path = '/Users/olivierdonze/switchdrive/COURS/Strategie_comm_2024/photos'
    path = '/Users/olivierdonze/switchdrive/COURS/Cinema4D_niv2_2024/photos'
    lst = glob(path+'/*.jpg')

    dlg = MyDialog(lst)
    dlg.Open(c4d.DLG_TYPE_ASYNC, defaultw=200, defaulth=200)