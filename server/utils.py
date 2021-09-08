import xml.etree.ElementTree as ET
import requests

""""

Utils to help u get up to date currencies rates 

returns: 

Dict in the form

USD 1.1215
JPY 121.03
BGN 1.9558
CZK 25.534

etc
"""


def get_currencies():
    r = requests.get(
        'http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml', stream=True)

    tree = ET.parse(r.raw)
    root = tree.getroot()

    namespaces = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}

    currency_dict = {}
    currency_dict["EUR"] = float(1.0000)

    for cube in root.findall('.//ex:Cube[@currency]', namespaces=namespaces):

        #print(cube.attrib['currency'], cube.attrib['rate'])
        currency_dict[str(cube.attrib['currency'])
                      ] = float(cube.attrib['rate'])

    return currency_dict


get_currencies()
