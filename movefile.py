import os


class Movefile:

    def __init__(self, megafile):
        self.megafile = megafile

    def move_file(self, dir_selected, critere):

        list_tag = []
        motsinterdits = [',', ':', '/', '*', '?', '<', '>', '|', '\\','.','"']
        critere = critere.split(',')

        for element in critere:
            try:
                tag = self.megafile.get_tag(element)
                tag = tag[0] if len(tag) == 1 else tag
                for item in motsinterdits:
                    if item in tag:
                        tag = str(tag).replace(item, ' ')

                list_tag.append(tag.strip())
            except (TypeError,IndexError) as e:
                print('{}'.format(e))
                print('Valeur spécifiée non reconnue. Un dossier correspondant -unknown- sera crée')
                list_tag.append('unknown {}'.format(element))
                continue

        dir_dest = os.path.join(dir_selected, *list_tag, os.path.basename(self.megafile.get_url()))

        try:
            dir_dest = copie(dir_dest)
            os.renames(self.megafile.get_url(), dir_dest)
        except (PermissionError, FileNotFoundError, TypeError) as e:
            print('{}'.format(e))
            return


def copie(url):
    i = 1
    if os.path.exists(url):
        url = url.split('.')
        url = ''.join(url[0:-1])+'{}'.format(i)+url[-1]
        i += 1
        copie(url)
    else:
        return url
