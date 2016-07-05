import os


class Movefile:

    def __init__(self, fichier):
        self.fichier = fichier




    def movefile(self, destination, critere):

        listetag=[]
        motsinterdits=[',', ':', '/', '*', '?', '<', '>', '|', '\\','.','"']

        critere = critere.split(',')

        for element in critere:
            try:
                tag = self.fichier.get_tag(element)
                tag = tag[0] if len(tag) == 1 else tag
                for item in motsinterdits:
                    if item in tag:
                        tag = str(tag).replace(item, ' ')

                listetag.append(tag.strip())
            except (TypeError,IndexError) as e:
                print('{}'.format(e))
                print('Valeur spécifiée non reconnue. Un dossier correspondant -unknown- sera crée')
                listetag.append('unknown {}'.format(element))
                continue

        foldest = os.path.join(destination, *listetag, os.path.basename(self.fichier.get_url()))

        try:
            foldest=copie(foldest)
            os.renames(self.fichier.get_url(), foldest)
        except (PermissionError,FileNotFoundError,TypeError) as e:
            print('{}'.format(e))
            return

def copie(url):
    i=1
    if os.path.exists(url):
        url=url.split('.')
        url =''.join(url[0:-1])+'{}'.format(i)+url[-1]
        i+=1
        copie(url)
    else:
        return url