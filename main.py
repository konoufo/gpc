import os,re
from finder import Finder
from movefile import Movefile
import time
import sys,ast,json
from devine import Devine


def find():

    url=''
    profondeur=''
    while not os.path.isdir(url):
        print('Must be dir')
        url=input('adresse du dossier:')
    while profondeur != '1' and profondeur != '2':
        print('1 dossier et sous dossier ; 2 dossier')
        profondeur=input('profondeur du dossier:')

    return Finder(url).dig(profondeur)

"""return activefiles"""


def doublon(activefiles):
    print('Looking for identical files')
    listedoublon = []
    for element in activefiles:
        for element1 in activefiles:
            if element.get_url() != element1.get_url():
                if element.get_extension() == element1.get_extension():
                    if element.get_tag('size') == element1.get_tag('size'):
                        with open(element.get_url(),'rb') as text1:
                            value1=text1.read(20)
                        with open(element.get_url(),'rb') as text2:
                            value2 = text2.read(20)
                        if value1 == value2:
                            if element.issame(element1.get_url()):
                                listedoublon.append(element1)
                                activefiles.remove(element1)
                                print(element.get_url(),'=',element1.get_url())
        if element in activefiles:
            activefiles.remove(element)

    print(len(listedoublon),'identical file(s)')
    if len(listedoublon) > 0:
        for element in listedoublon:
            print(element.get_name())
    return listedoublon


def byname(activefiles,value):
    text = value.lower()
    text = text.split(' ')
    text = '.*' + '.*'.join(text) + '.*'
    result=[]
    for element in activefiles:
        if re.match(text, element.get_name().lower()):
            result.append(element)
    return result


def bysize(activefiles):
    finallist = []
    mini=int(input('Valeur minimale :'))
    maxi = int(input('Valeur maximale:'))
    for element in activefiles:
        if maxi > element.get_tag('size') > mini:
            finallist.append(element)
    return finallist


def byattribute(activefiles):
    finallist = []

    attribute = input('attribute')
    value = input('value')
    for element in activefiles:
        if element.get_tag(attribute) == value:
            finallist.append(element)
    return finallist

"""Change activefiles"""


def delete(activefiles):

    for element in activefiles:
        if os.path.exists(element.get_url()):
            element.delete()


def movefile(activefiles):

    listetags = input('How ?')

    if get_preference('Default folder'):
        foldest = get_preference('Default folder')

    else:
        foldest = input('Destination:')

    for element in activefiles:
         Movefile(element).movefile(foldest, listetags)


def rename(activefiles,value):

    if len(activefiles)>1:
        print('Plusieurs fichiers auront le meme nom. Veuillez choisir un ordre de numérotation')
        for element in activefiles:
            number=input(element.get_name())
            val=number+' '+value+'.'+element.get_extension()
            element.rename(val)

"""Options"""


def actionhelp():
    print('---------------')
    print('Write one of these keywords : '
          '\ndoublon :'
          '\nmovefile : help you to move one file or more by using tags. You may read the documentation to know whitch tag matches with whitch file.'
          '\ndelete : delete all files on the screen. '
          '\nfind : get all files in the specified folder.'
          '\nshowmeta : get info'
          '\nchangemeta : change info'
          '\nexit :  stop the programm'
          '\ndoc : to see the doc')
    print('---------------')


def set_preference():
    with open('preference.txt', 'rb') as docprefread:
        dict = docprefread.read().decode('utf-8')
    dict = ast.literal_eval(dict)
    for element in dict.keys():
        pref=input(element+':')
        dict[element] = pref
    with open('preference.txt', 'wb') as docprefwrite:
        dicstr = json.dumps(dict).encode('utf-8')
        docprefwrite.write(bytes(dicstr))


def get_preference(pref):
    with open('preference.txt', 'rb') as docpref:
        dict = ast.literal_eval(docpref.read().decode('utf-8'))
        if dict[pref] == "":
            return
        else:
            return dict[pref]


"""Metadata"""


def show_meta(activefiles):

    for element in activefiles:
        print ('File name:',element.get_name())
        for item in element.get_alltag():
            print(item[0],'|',item[1],'||',end='')
        print('')
        print('---------------')


def change_meta(activefiles):
    print('Write "Stop" to interrupt the process')

    for element in activefiles:
        for item in element.get_tagkeys():
            value=element.get_tag(item)
            tagvalue=input(element.get_name()+' '+item+' value :'+str(value)+'. Change in :')
            if tagvalue == 'stop':
                print('Fin')
                return
            element.change_tag(item,tagvalue)


def update(activefiles):
    for element in activefiles:
        Devine(element).update_arc()


def main():
    """
    url=r'C:\Users\Jack\Music\arctestmp3'
    profondeur='1'
    foldest=r'C:\Users\Jack\Music\destarctestmp3'
    listetags='artists,album'

    activefiles=find(url,profondeur)
    #update(activefiles)
    movefile(activefiles,listetags,foldest)
    """

    action=''
    activefiles = find()
    actionhelp()
    while action != 'exit':

        action = input('action:')

        if action == 'find':
            activefiles = find()

        elif action == 'doublon':
            activefiles = doublon(activefiles)

        elif action == 'byattri':
            activefiles=byattribute(activefiles)

        elif action == 'bysize':
            activefiles = bysize(activefiles)

        elif action == 'byname':
            value=input('value: ')
            activefiles = byname(activefiles,value)

        elif action == 'movefile':
            movefile(activefiles)

        elif action == 'delete':
            delete(activefiles)

        elif action == 'showmeta':
            show_meta(activefiles)

        elif action == 'changemeta':
            change_meta(activefiles)

        elif action == 'update':
            update(activefiles)

        elif action == 'help':
             actionhelp()

        elif action== 'doc':
            os.startfile('info.txt')

    print('fin du game')

main()