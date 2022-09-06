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