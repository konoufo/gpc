import re


def rename(methode,liste,value):

    if methode == 'garde':
        text = value.lower()
        text = text.split(' ')
        text = '.*' + '.*'.join(text) + '.*'
        for element in liste:
            if re.match(text,element.lower()):
                a=re.match(text,element.lower()).group()
                print(a)

    elif methode == 'remove':
        for element in liste:
            if value in element:
                print(element)
                print(element.replace(value,''))

def byname(activefiles,value):
    text = value.lower()
    text = text.split(' ')
    text = '.*' + '.*'.join(text) + '.*'
    result=[]
    for element in activefiles:
        if re.match(text, element.get_name().lower()):
            result.append(element)
    return result

def renam(activefiles,value):

    if len(activefiles)>1:
        print('Plusieurs fichiers auront le meme nom. Veuillez choisir un ordre de numérotation')
        for element in activefiles:
            number=input(element.get_name())
            val=number+' '+value+'.'+element.get_extension()
            element.rename(val)


from finder import Finder
url=r'C:\Users\Jack\Videos'
print(renam(byname(Finder(url).dig('1'),'one punch man'),'one punch man'))