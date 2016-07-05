

class Traducteur():


    def __init__(self,ext):
        self.ext=ext

    def get_trad(self,tag):
        with open('traducteur.txt') as text:

            text = text.read().replace('\n', '')
            text = text.replace('sym','©')
            traducteur =text.split(';;')

        listetrad = []

        for element in traducteur:
            el = element.split(';')
            listetrad.append(el)
        for element in listetrad:
            if element[0] == self.ext.lower():
                if element[1]==tag:
                    return str(element[2])

    def accept_tag(self):
        with open('traducteur.txt') as text:
            text = text.read().replace('\n', '')
            text = text.replace('sym', '©')
            text = text.split(';;')

        listetag=[]
        for element in text:
            el=element.split(';')
            if el[0]==self.ext:
                listetag.append(el[1])
        return listetag

