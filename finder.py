import os
import megafile


class Finder:

    def __init__(self, url):
        self.url = url

    def dig(self, deep):

        dossier = self.url

        listurl = []
        self.listurl = listurl

        if deep == '1':     # dossier et sous-dossier
            for path, dirs, files in os.walk(dossier):
                for filename in files:
                    url = os.path.join(path, filename)
                    if os.path.isfile(url):
                        if megafile.Megafile(url).isaccepted():
                            self.listurl.append(megafile.Megafile(url))
                            print('\r','Nombre de fichier trouvé:', len(self.listurl), end='')

        elif deep == "2":      # dossier
            for filename in os.listdir(dossier):
                url = os.path.join(dossier, filename)
                if os.path.isfile(url):
                    if megafile.Megafile(url).isaccepted():
                        self.listurl.append(megafile.Megafile(url))
                        print('\r', 'Nombre de fichier trouvé:', len(self.listurl), end='')
        print()
        return listurl

