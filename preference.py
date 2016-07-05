import ast
import json


class Preference():

    # enregistre et envoie les preferences de l'utilisateur
    # dossier par defaut pour chaque type


    def __init__(self):
        self=None



    def get_pref(self,pref):
        with open('preference.txt', 'rb') as docpref:
            dict= ast.literal_eval(docpref.read().decode('utf-8'))
            if dict[pref]=="":
                return
            else:
                return dict[pref]


    def set_pref(self,pref,value):
        with open('preference.txt', 'rb') as docprefread:
            dict =docprefread.read().decode('utf-8')
        dict = ast.literal_eval(dict)
        dict[pref]=value
        with open('preference.txt','wb') as docprefwrite:
            dicstr = json.dumps(dict).encode('utf-8')
            docprefwrite.write(bytes(dicstr))

    def reset_pref(self):
        liste = ['Default folder', ]
        for a in liste:
            Preference().set_pref(a, '')


