from pyquery import PyQuery
import requests
def get_info(object):
    obj = object.replace(' ', '%20')
    parsed_html = PyQuery(requests.get('http://simbad.u-strasbg.fr/simbad/sim-id?Ident=' + obj).content)
    infobox = parsed_html("#basic_data").find('table').find('tr').find('b').find('tt').find('font')
    redshift = str(infobox).split('(~) ')[1].split(' ')[0].strip()
    speed = str(infobox).split('(km/s) ')[1].split(' ')[0].strip()
    return [redshift, speed]