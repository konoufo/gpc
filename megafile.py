import filecmp
import os
import shutil
import mutagen
from exiftool import ExifTool
from exiftool import fsencode
from mutagen import asf
from mutagen import mp4
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from pymediainfo import MediaInfo
from traducteur import Traducteur


class Megafile:

    def __init__(self, url):
        self.url = url

    def get_types(self):

        with open('ext.txt', 'rb') as text:
            ext_list = text.read().decode('utf-8').replace('\n', '').split(';;')
        for element in ext_list:
            if element.split(';')[0] == self.get_extension():
                extension = element.split(';')[0]
                soustype = element.split(';')[1]
                type = element.split(';')[3]
                constructeur=element.split(';')[2]
                return extension, soustype, type,constructeur

    def get_extension(self):
        return self.url.split('.')[-1].lower()
    
    def issame(self, file_cmp):
        return filecmp.cmp(self.url, file_cmp)

    def rename(self, new_name):
        src_folder = os.path.dirname(self.url)
        dest = os.path.join(src_folder,new_name)
        if os.path.exists(dest):
            print('Erreur. Le fichier existe déjà')
        else:
            shutil.move(self.url, dest)

    def delete(self):
        try:
            os.remove(self.url)
        except PermissionError as e:
            print(e)

    def get_name(self):
        return os.path.basename(self.url)

    def get_url(self):
        return os.path.abspath(self.url)
    
    def get_tag(self, tag):  # renvoie le tag demandé

        if tag == 'type':
            try:
                return self.get_types()[2]
            except TypeError:
                print('TypeError', self.url)
                pass

        elif tag == 'st':
            try:
                return self.get_types()[1]
            except TypeError:
                print('TypeError', self.url)
                pass

        elif tag == 'constructor':
            try:
                return self.get_types()[3]
            except TypeError:
                print('TypeError', self.url)
                pass

        elif tag == 'ext':
            return self.get_extension()

        elif tag == 'size':
            return os.path.getsize(self.url)

        else:
            tag = Traducteur(self.get_extension()).get_trad(tag)
            if self.get_extension() == 'mp3':
                try:
                    ID3(self.url).update_to_v23()
                    file = EasyID3(self.url)
                    return file.get(tag)
                except AttributeError as e:
                    print(e)
                    pass
                except PermissionError as e:
                    print(e)
                    pass
                except mutagen.id3._util.ID3NoHeaderError as e:
                    print(e)
                    pass

            elif self.get_extension() == 'mp4':
                try:
                    file = mp4.Open(self.url)
                    return file.get(tag)
                except mutagen.mp4.MP4StreamInfoError:
                    print('mutagen.mp4.MP4StreamInfoError', self.url)
                    pass

            elif self.get_extension() == 'wmv':
                file = asf.Open(self.url)
                return file.get(tag)

            elif self.get_extension() == 'pdf':
                with ExifTool() as et:
                    file = et.get_metadata(self.url)
                    return file.get(tag)

            """
            else:
                for element in MediaInfo.parse(self.url).to_data()['tracks']:
                    for el in sorted(element):
                        if el == tag:
                            return element[tag]
            """

    def change_tag(self, tag, tagvalue):

        tag = Traducteur(self.get_extension()).get_trad(tag)

        if self.get_extension() == 'mp3':
            try:
                ID3(self.url).update_to_v23()
                ID3(self.url).save()
                file = EasyID3(self.url)
                file[tag] = tagvalue
                file.save()
            except (mutagen.id3._util.ID3NoHeaderError, PermissionError) as e:
                print(e)
                return

        elif self.get_extension() == 'mp4':
            file = mp4.Open(self.url)
            file[tag] = tagvalue
            file.save()

        elif self.get_extension() == 'wmv':
            file = asf.Open(self.url)
            file[tag] = tagvalue
            file.save()

        elif self.get_extension() == 'pdf':
            with ExifTool() as et:
                params = map(fsencode, ['-' + tag + '=' + "%s" % tagvalue, '%s' % self.url])
                et.execute(*params)

    """def get_taglist(self):

        if self.get_extension() =='pdf':
            with ExifTool() as et:
                liste_extension = et.get_metadata(self.url)
                return liste_extension.keys()

        elif self.get_extension() == 'mp3':
            liste_extension = EasyID3(self.url)
            return liste_extension.keys()

        elif self.get_extension() == 'mp4':
            liste_extension = mp4.Open(self.url)
            return liste_extension.keys()

        elif self.get_extension() == 'wmv':
            liste_extension = asf.Open(self.url)
            return liste_extension.keys()

        else:
            liste_extension = []
            for element in MediaInfo.parse(self.url).to_data()['tracks']:
                for el in element.keys():
                    liste_extension.append(el)
            return liste_extension
    """

    def get_alltag(self):
        result = []
        for element in Traducteur(self.get_extension()).accept_tag():
            result.append((element, self.get_tag(element)))
        return result

    def get_tagkeys(self):
        result = []
        for element in Traducteur(self.get_extension()).accept_tag():
            result.append(element)
        return result

    def isaccepted(self):
        with open('ext.txt','rb') as text:
            ext_list = text.read().decode('utf-8').replace('\n', '').split(';;')
        for element in ext_list:
            if element.split(';')[0] == self.get_extension():
                return True