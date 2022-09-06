import astropy.units as u
import astropy.cosmology.units as cu
from astropy.cosmology import WMAP9
from astropy import constants as const
import pic_processing
import getobjectinfo
import sys
custom = False
d = 0
zo = 0
new_d = 0
new_zo = 0
img_addr = ''
def convert(data):
    data_arr = data.split(' ')
    mode = data_arr[0]
    img_addr = data_arr[1]
    if mode == '-o':
        obj_name = data_arr[2]
        data_obj = getobjectinfo.get_info(obj_name)
        if data == None:
            sys.exit()
        zo = float(data_obj[0]) * cu.redshift
        v = float(data_obj[1]) * u.kilometer / u.second
        zd = v / const.c * cu.redshift
        zd = zd.decompose()
        zo = zo.decompose()
        z = (zo - zd)
        d = z.to(u.Mpc, cu.redshift_distance(WMAP9))
        new_v = float(data_arr[3]) * u.meter / u.second
        new_d = float(data_arr[4]) * u.Mpc
        new_zd = new_v / const.c * cu.redshift
        new_z = new_d.to(cu.redshift, cu.redshift_distance(WMAP9))
        new_z = new_z.decompose()
        new_zd = new_z.decompose()
        new_zo = (new_z + new_zd)       
    elif mode == 'info':
        print('This tool is made to edit images of astronomical object using different redshifts, distances, etc.\nUsage: insert a string "[mode] [image address] [object data] [new view point data]" \n mode should be -o (working with object name, in [object data] only object name is specified), -c (working with custom object, [object data] should be radial velocity (in m/s) and distance (in Mpc)) \n New PoV data should be: new radial velocity and new distance')
    elif mode == '-c':
        v = float(data_arr[2]) * u.meter / u.second# distance
        d = float(data_arr[3]) * u.Mpc # radial velocity (in m/s), v << c
        z = d.to(cu.redshift, cu.redshift_distance(WMAP9)) # cosmological redshift
        zd = v / const.c * cu.redshift # doppler redshift
        zo = z + zd # total redshift
        new_v = float(data_arr[4]) * u.meter / u.second
        new_d = float(data_arr[5]) * u.Mpc
        new_zd = new_v / const.c * cu.redshift
        new_z = new_d.to(cu.redshift, cu.redshift_distance(WMAP9))
        new_z = new_z.decompose()
        new_zd = new_z.decompose()
        new_zo = (new_z + new_zd)
    else:
        print('Wrong mode. Please try again.')
    pic_processing.GetOriginalImage(img_addr, zo.value)
    thenewimagename = pic_processing.ApplyChanges(new_zo.value)
    pic_processing.ApplyDistance(thenewimagename, d.value, new_d.value)
    print('Done! Your new image is called "' + thenewimagename + '"')