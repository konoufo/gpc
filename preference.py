import ast
import json


class Preference:

    def __init__(self):
        self = None

    def get_pref(self, pref):
        with open('preference.txt', 'rb') as doc_read:
            dict= ast.literal_eval(doc_read.read().decode('utf-8'))
            if dict[pref] == "":
                return
            else:
                return dict[pref]

    def set_pref(self, pref, value):
        with open('preference.txt', 'rb') as doc_read:
            dic =doc_read.read().decode('utf-8')
        dic = ast.literal_eval(dic)
        dic[pref]=value
        with open('preference.txt', 'wb') as doc_write:
            dic_str = json.dumps(dic).encode('utf-8')
            doc_write.write(bytes(dic_str))

    def reset_pref(self):
        result = ['Default folder', ]
        for a in result:
            Preference().set_pref(a, '')


