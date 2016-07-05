from pymediainfo import MediaInfo
from exiftool import ExifTool
url=r'C:\Users\Jack\Music\mp3 complet'
url1=r'C:\Users\Jack\Documents\fichier pro\doctest'
from finder import Finder


"""
for element in Finder(url1).dig('1'):
a=MediaInfo.parse(element.get_url()).to_data()['tracks'][0]
if element.get_extension()=='doc':
print(a.keys())
"""

url3=r'C:\Users\Jack\Documents\fichier\Documents à trier\Documents word'
for element in Finder(url3).dig('1'):
    if element.get_extension() == 'docx':
        with ExifTool() as et:
            file = et.get_metadata(element.get_url())
        if 'XMP:Title'in file.keys():
            print(file['XMP:Title'])
        else:
            print(element.get_url())