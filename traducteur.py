

class Traducteur():

    def __init__(self,ext):
        self.ext=ext

    def get_trad(self,tag):
        with open('traducteur.txt') as text:

            text = text.read().replace('\n', '')
            text = text.replace('sym','©')
            traducteur = text.split(';;')

        list_trad = []

        for element in traducteur:
            el = element.split(';')
            list_trad.append(el)
        for element in list_trad:
            if element[0] == self.ext.lower():
                if element[1] == tag:
                    return str(element[2])

    def accept_tag(self):
        with open('traducteur.txt') as text:
            text = text.read().replace('\n', '')
            text = text.replace('sym', '©')
            text = text.split(';;')

        list_tag = []
        for element in text:
            el = element.split(';')
            if el[0] == self.ext:
                list_tag.append(el[1])
        return list_tag

