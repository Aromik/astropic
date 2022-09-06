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
def ApplyDistance(image_address, old_dist, new_dist):
    ipath = Path(image_address)
    img = Image.open(ipath)
    basewidth = img.size[0] * old_dist / new_dist 
    basewidth = round(basewidth)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
    img.save(image_address)