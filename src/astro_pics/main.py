import astropy.units as u
import astropy.cosmology.units as cu
from astropy.cosmology import WMAP9
from astropy import constants as const
import sys
from PIL import Image
import os
from pathlib import Path
def wav2hue(wavelength):
    hue = (750 - wavelength) / 9.9346
    return hue
def hue2wav(hue):
    wavelength = 750 - 9.9346 * hue
    return wavelength
newname = ''
def GetOriginalImage(image_address, redshift):
    #get each pixel data, then change it to what is needed, to get the orig image
    ipath = Path(image_address)
    img = Image.open(ipath)
    img_hsv = img.convert('HSV')
    pixels = img_hsv.load()
    for i in range(img.size[0]): # for every pixel:
        for j in range(img.size[1]):
            hue = pixels[i,j][0]
            sat = pixels[i,j][1]
            val = pixels[i,j][2]
            wave = hue2wav(hue)
            newwave = wave / (redshift + 1)
            newhue = wav2hue(newwave)
            newhue = round(newhue)
            pixels[i,j] = (newhue, sat, val)
    img_rgb = img_hsv.convert('RGB')
    global newname
    newname = image_address.split('.')[0] + '_orig.' + image_address.split('.')[1]
    img_rgb.save(newname)
def ApplyChanges(new_redshift):
   #get each pixel data, then change it to what is needed, to get the orig image
    image_orig = newname
    ipath = Path(image_orig)
    img = Image.open(ipath)
    img_hsv = img.convert('HSV')
    pixels = img_hsv.load()
    for i in range(img.size[0]): # for every pixel:
        for j in range(img.size[1]):
            hue = pixels[i,j][0]
            sat = pixels[i,j][1]
            val = pixels[i,j][2]
            wave = hue2wav(hue)
            newwave = wave * (new_redshift + 1)
            newhue = wav2hue(newwave)
            newhue = round(newhue)
            pixels[i,j] = (newhue, sat, val)
    img_rgb = img_hsv.convert('RGB')
    img_rgb.save(image_orig.split('_orig')[0] + '_new.' + image_orig.split('.')[1])
    os.remove(newname)
    return image_orig.split('_orig')[0] + '_new.' + image_orig.split('.')[1]
'''def ApplyDistance(image_address, old_dist, new_dist):
    ipath = Path(image_address)
    img = Image.open(ipath)
    basewidth = img.size[0] * old_dist / new_dist 
    basewidth = round(basewidth)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
    img.save(image_address)'''
custom = False
d = 0
zo = 0
new_d = 0
new_zo = 0
img_addr = ''
from pyquery import PyQuery
import requests
def get_info(object):
    obj = object.replace(' ', '%20')
    parsed_html = PyQuery(requests.get('http://simbad.u-strasbg.fr/simbad/sim-id?Ident=' + obj).content)
    infobox = parsed_html("#basic_data").find('table').find('tr').find('b').find('tt')
    try:
        redshift = str(infobox).split('z(')[1].strip().split(' ')[1]#.split(' ')[0].strip()
        speed = str(infobox).split('(km/s) ')[1].split(' ')[0].strip()
        return [redshift, speed]
    except IndexError:
        print('Your object doesnt have required data (radial valocity and redshift) in the SIMBAD database. Try again with running as a custom object')
        return None
def convert(data):
    data_arr = data.split(' ')
    mode = data_arr[0]
    global img_addr
    global zo
    global zd
    global d
    global v
    global z
    global new_v
    global new_d
    global new_zd
    global new_zo
    global new_z
    global thenewimagename
    if mode == '-o':
        img_addr = data_arr[1]
        obj_name = data.split('"')[1].split('"')[0]
        data_arr = data.split('"')[2].strip().split(' ')
        data_obj = get_info(obj_name)
        if data == None:
            sys.exit()
        zo = float(data_obj[0]) * cu.redshift
        v = float(data_obj[1]) * u.kilometer / u.second
        zd = v / const.c * cu.redshift
        zd = zd.decompose()
        zo = zo.decompose()
        z = (zo - zd)
        d = z.to(u.Mpc, cu.redshift_distance(WMAP9))
        new_v = float(data_arr[0]) * u.meter / u.second
        new_d = float(data_arr[1]) * u.Mpc
        new_zd = new_v / const.c * cu.redshift
        new_z = new_d.to(cu.redshift, cu.redshift_distance(WMAP9))
        new_z = new_z.decompose()
        new_zd = new_z.decompose()
        new_zo = (new_z + new_zd)       
    elif mode == 'info':
        sys.exit('This tool is made to edit images of astronomical object using different redshifts, distances, etc.\nUsage: insert a string "[mode] [image address] [object data] [new view point data]" \n mode should be -o (working with object name, in [object data] only object name is specified (the name should be inside of " ")), -c (working with custom object, [object data] should be radial velocity (in m/s) and distance (in Mpc)) \n New PoV data should be: new radial velocity and new distance')
    elif mode == '-c':
        img_addr = data_arr[1]
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
    GetOriginalImage(img_addr, zo.value)
    thenewimagename = ApplyChanges(new_zo.value)
    # ApplyDistance(thenewimagename, d.value, new_d.value)
    # The function has been deprecated
    print('Done! Your new image is called "' + thenewimagename + '"')