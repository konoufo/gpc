# -:- coding: utf-8 -:-
import os, re
from finder import Finder
from movefile import Movefile
import time
import sys, ast, json
from devine import Devine


def find():

    url = ''
    deep = ''
    while not os.path.isdir(url):
        print('Doit etre un dossier')
        url = input('adresse du dossier:')
    while deep != '1' and deep != '2':
        print('1 dossier et sous dossier ; 2 dossier')
        deep = input('profondeur du dossier:')

    return Finder(url).dig(deep)

"""return active_files"""


def doublon(active_files):

    print('Looking for identical files')
    result = []

    for element in active_files:
        for element1 in active_files:
            if element.get_url() != element1.get_url():
                if element.get_extension() == element1.get_extension():
                    if element.get_tag('size') == element1.get_tag('size'):
                        with open(element.get_url(), 'rb') as text1:
                            value1 = text1.read(20)
                        with open(element.get_url(), 'rb') as text2:
                            value2 = text2.read(20)
                        if value1 == value2:
                            if element.issame(element1.get_url()):
                                result.append(element1)
                                active_files.remove(element1)
                                print(element.get_url(), '=', element1.get_url())
        if element in active_files:
            active_files.remove(element)

    return result

# todo: rename functions match_by_name, match_by_size and so on
def byname(active_files, value):
    text = value.lower()
    text = text.split(' ')
    text = '.*' + '.*'.join(text) + '.*'
    result = []
    for element in active_files:
        if re.match(text, element.get_name().lower()):
            result.append(element)
    return result


def bysize(active_files):
    result = []
    mini = int(input('Valeur minimale :'))
    maxi = int(input('Valeur maximale:'))
    for element in active_files:
        if maxi > element.get_tag('size') > mini:
            result.append(element)
    return result


def byattribute(active_files):
    result = []
    attribute = input('attribut')
    value = input('valeur')
    for element in active_files:
        if element.get_tag(attribute) == value:
            result.append(element)
    return result

"""Change active_files"""


def delete(active_files):
    for element in active_files:
        if os.path.exists(element.get_url()):
            element.delete()


def move_file(active_files):

    list_tags = input('How ?')

    if get_preference('Default folder'):
        folder_destination = get_preference('Default folder')

    else:
        folder_destination = input('Destination:')

    for element in active_files:
        Movefile(element).move_file(folder_destination, list_tags)


def rename(active_files,value):
    # value nom sans ext
    if len(active_files) > 1:
        print('Plusieurs fichiers auront le meme nom. Veuillez choisir un ordre de numérotation')
        for element in active_files:
            number = input(element.get_name())
            val = value+' '+number+'.'+element.get_extension()
            element.rename(val)

"""Options"""


def action_help():
    print('---------------')
    print('Write one of these keywords : '
          '\nfind : '
          '\ndoublon :'
          '\nmove_file : '
          '\ndelete : '
          '\nshowmeta :'
          '\nchangemeta :'
          '\nexit :'
          '\ndoc : ')
    print('---------------')


def set_preference():
    with open('preference.txt', 'rb') as doc_read:
        dic = doc_read.read().decode('utf-8')
    dic = ast.literal_eval(dic)
    for element in dic.keys():
        pref = input(element+':')
        dic[element] = pref
    with open('preference.txt', 'wb') as doc_write:
        dic_str = json.dumps(dic).encode('utf-8')
        doc_write.write(bytes(dic_str))


def get_preference(pref):
    with open('preference.txt', 'rb') as doc:
        dic = ast.literal_eval(doc.read().decode('utf-8'))
        if dic[pref] == "":
            return
        else:
            return dic[pref]


"""Metadata"""


def show_meta(active_files):
    for element in active_files:
        print('File name:', element.get_name())
        for item in element.get_alltag():
            print(item[0], '|', item[1], '||', end='')
        print('')
        print('---------------')


def change_meta(active_files):
    print('Write "Stop" to interrupt the process')
    for element in active_files:
        for item in element.get_tagkeys():
            value=element.get_tag(item)
            tagvalue = input(element.get_name()+' '+item+' value :'+str(value)+'. Change in :')
            if tagvalue == 'stop':
                print('Fin')
                return
            element.change_tag(item, tagvalue)


def music_print(active_files):
    result_list = []
    for element in active_files:
        result_list.append((element, Devine(element).music_print(), 'music_print'))
    return result_list


def movie_tag(active_files):
    result = []
    for element in active_files:
        result.append(Devine(element).movie_tag())
    return result


def update_meta(update_list):

    for element in update_list:
        Devine(element[0]).update_tag(element[1], element[2])


def main():

    action = ''
    active_files = find()
    action_help()
    update_list = []
    while action != 'exit':

        action = input('action:')

        if action == 'find':
            active_files = find()

        elif action == 'doublon':
            active_files = doublon(active_files)

        elif action == 'byattri':
            active_files = byattribute(active_files)

        elif action == 'bysize':
            active_files = bysize(active_files)

        elif action == 'byname':
            value = input('value: ')
            active_files = byname(active_files, value)

        elif action == 'move_file':
            move_file(active_files)

        elif action == 'delete':
            delete(active_files)

        elif action == 'showmeta':
            show_meta(active_files)

        elif action == 'changemeta':
            change_meta(active_files)

        elif action == 'music_print':
            update_list = music_print(active_files)

        elif action == 'updatemeta':
            if len(update_list) > 0:
                update_meta(update_list)
            else:
                print("Rien a mettre à jour")

        elif action == 'help':
             action_help()

        elif action == 'doc':
            os.startfile('info.txt')

        elif action == 'activelist':
            print(len(active_files), 'fichiers')
            if len(active_files) > 0:
                for element in active_files:
                    print(element.get_url())

    print('fin du game')

main()