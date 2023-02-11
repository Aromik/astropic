import numpy as np
import matplotlib.image as imager
from astropy.io import fits
import sys
try:
    fitsfilename = sys.argv[1]
except IndexError:
    sys.exit('Usage: ' + sys.argv[0] + ' *Your .fits file address or URL*')
if (fitsfilename.split('/')[0] == 'http:') or (fitsfilename.split('/')[0] == 'https:'):
    # link, we need to download
    try:
        from astropy.utils.data import download_file
        image_file2 = download_file(fitsfilename, cache=True)
        hdu_list2 = fits.open(image_file2)
        Image_data2 = hdu_list2[0].data #here is hdu_list[0].data, not hdu_list[1].data
        hdu_list2.close()
        image_data2 = fits.getdata(image_file2)
        name = fitsfilename.split('/')[len(fitsfilename.split('/')) - 1]
        name = name[0: len(name) - 5]
        imager.imsave(name + '.png', image_data2, cmap='gray')
        print('Success! Your link has been processed')
    except Exception as e:
        print('Something went wrong! Here is the error:')
        print(e)
else:
    # not a link, using local protocol
    try:
        hdu_list = fits.open(fitsfilename, cache=True)
        Image_data = hdu_list[0].data #here is hdu_list[0].data, not hdu_list[1].data
        hdu_list.close()
        image_data = fits.getdata(fitsfilename, cache=True)
        name = fitsfilename
        name = name[0: len(name) - 5]
        imager.imsave(name + '.png', image_data, cmap='gray')
        print('Success! Your local file has been processed')
    except Exception as e:
        print('Something went wrong! Here is the error:')
        print(e)