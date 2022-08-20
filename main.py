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
try:
    mode = sys.argv[1]
    if mode == 'info':
        print('This tool is made to edit images of astronomical object using different redshifts, distances, etc.\nUsage: ' + sys.argv[0] + ' [mode] [image address] [object data] [new view point data] \n mode should be -o (working with object name, in [object data] only object name is specified), -c (working with custom object, [object data] should be radial velocity (in m/s) and distance (in Mpc)) \n New PoV data should be: new radial velocity and new distance')
    if mode == '-o':
        custom = False
    if mode == '-c':
        custom = True
    img_addr = sys.argv[2]
    if custom:
        v = float(sys.argv[3]) * u.meter / u.second# distance
        d = float(sys.argv[4]) * u.Mpc # radial velocity (in m/s), v << c
        z = d.to(cu.redshift, cu.redshift_distance(WMAP9)) # cosmological redshift
        zd = v / const.c * cu.redshift # doppler redshift
        zo = z + zd # total redshift
        new_v = float(sys.argv[5]) * u.meter / u.second
        new_d = float(sys.argv[6]) * u.Mpc
        new_zd = new_v / const.c * cu.redshift
        new_z = new_d.to(cu.redshift, cu.redshift_distance(WMAP9))
        new_z = new_z.decompose()
        new_zd = new_z.decompose()
        new_zo = (new_z + new_zd)
    else:
        obj_name = sys.argv[3]
        data = getobjectinfo.get_info(obj_name)
        zo = float(data[0]) * cu.redshift
        v = float(data[1]) * u.kilometer / u.second
        zd = v / const.c * cu.redshift
        zd = zd.decompose()
        zo = zo.decompose()
        z = (zo - zd)
        d = z.to(u.Mpc, cu.redshift_distance(WMAP9))
        new_v = float(sys.argv[4]) * u.meter / u.second
        new_d = float(sys.argv[5]) * u.Mpc
        new_zd = new_v / const.c * cu.redshift
        new_z = new_d.to(cu.redshift, cu.redshift_distance(WMAP9))
        new_z = new_z.decompose()
        new_zd = new_z.decompose()
        new_zo = (new_z + new_zd)
except IndexError:
    sys.exit('Usage: ' + sys.argv[0] + ' [mode] [image address] [object data]. For more info run ' + sys.argv[0] + ' info')
#redact the distance
pic_processing.GetOriginalImage(img_addr, zo.value)
thenewimagename = pic_processing.ApplyChanges(new_zo.value)
print('Done! Your new image is called "' + thenewimagename + '"')