import c4d
import sys


CONTAINER_ORIGIN =1026473

#TODO : gérer les grilles non générées pas l'import ascii
#TODO : si on a des nodata compléter le grille !
#TODO : gérer les maille non carrées quand dim_cell_x != dim_cell_z

def tri_pts_sens_mnt(op,origin):
    mg = op.GetMg()
    #on inverse le z pour que ce soit dans le sens mnt !
    vec2tuple = lambda v : (-v.z,v.x,v.y)
    pts_temp = [vec2tuple(p*mg) for p in op.GetAllPoints()]
    pts_temp.sort()
    
    tuple2vec = lambda z,x,y : c4d.Vector(x,y,-z)
    pts = [tuple2vec(z,x,y)+origin for z,x,y in pts_temp]
    return pts

def export_mnt_ascii(mnt,fn_dst,origin):
    #mg = mnt.GetMg()
    pts= tri_pts_sens_mnt(mnt,origin)
    #pts = [p*mg+origin for p in mnt.GetAllPoints()]

    #dimension cellule en x
    dim_cell_x = pts[1].x - pts[0].x

    #calcul nombre de colonnes
    ncols = 0
    #predz = sys.float_info.min
    for i,p in enumerate(pts):
        if i==0:
            pred = p
        else:
            if p.z != pred.z:
                ncols = i
                break
    #print(ncols)

    #dimension cellule en z
    dim_cell_z = pts[ncols].z - pts[0].z

    #calcul nombre de lignes
    nrows = 1
    pred = pts[0]
    for i in range(0,len(pts),ncols):
        if i >0:
            size_z = pts[i].z - pred.z
            if round(size_z,5)== round(dim_cell_z,5):
                pred = pts[i]
                nrows+=1
            else:
                break

    nb_pts = ncols*nrows

    xllcorner = pts[0].x - dim_cell_x/2
    yllcorner = pts[nb_pts-1].z + dim_cell_z/2

    #print(xllcorner,yllcorner)



    with open(fn_dst,'w') as f:
        f.write(f'ncols         {ncols}\n')
        f.write(f'nrows         {nrows}\n')
        f.write(f'xllcorner     {xllcorner}\n')
        f.write(f'yllcorner     {yllcorner}\n')
        f.write(f'cellsize      {dim_cell_x}\n')
        f.write(f'NODATA_value  -9999\n')


        for i,p in enumerate(pts[:nb_pts]):
            #écriture de l'altitude'
            f.write(str(p.y))

            #si on n'est pas à la fin de la grille en x on met un espace
            #sinon un saut de paragraphe
            if (i+1)%(ncols):
                f.write(' ')
            else:
                f.write('\n')
    return True




# Main function
def main():
    mnt = op
    #fn_dst = '/Users/olivierdonze/Documents/TEMP/Chatelard/swisstopo/test_mnt_asci.asc'
    fn_dst = c4d.storage.LoadDialog(title='', flags=c4d.FILESELECT_SAVE, force_suffix='asc')

    #print(fn_dst)

    if not fn_dst : return
    origin = doc[CONTAINER_ORIGIN]
    export_mnt_ascii(mnt,fn_dst,origin)

# Execute main()
if __name__=='__main__':
    main()