import requests,ast,json,xmltodict
from acrcloud.recognizer import ACRCloudRecognizer


class Devine:

    def __init__(self,fichier):
        self.fichier=fichier

    def book_tag(self,param):

        livre = 'https://www.goodreads.com/search.xml?key=bIlqMcaq64Bw2zLbZmYDXQ&q='
        link = livre+param
        dict = ast.literal_eval(json.dumps(xmltodict.parse(requests.get(link).text)))
        result=[]
        for item in dict['GoodreadsResponse']['search']['results']['work']:
            result.append((item['best_book']['title'],item['best_book']['author']['name']))
        return result

    def movie_tag(self,param):

        end_url=[]
        link = r'http://www.omdbapi.com/?'
        dictionnaire = ast.literal_eval(param)
        for item in dictionnaire.keys():
            a = '&' + item + '=' + dictionnaire[item]
            end_url.append(a)
        link = link + ''.join(end_url)
        result = requests.get(link).text
        return result

    def musique_tag(self):

        # tag : artist, title, genre, album, label

        config = {
            'host': 'us-west-2.api.acrcloud.com',
            'access_key': '',
            'access_secret': '',
            'debug': False,
            'timeout': 10  # seconds
        }

        '''This module can recognize ACRCloud by most of audio/video file.
            Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
            Video: mp4, mkv, wmv, flv, ts, avi ...'''

        re = ACRCloudRecognizer(config)
        dict1 = ast.literal_eval(re.recognize_by_file(self.fichier.get_url(), 0))

        if dict1['status']['msg'] == 'Success' and dict1['metadata'] and dict1['metadata']['music'][0]:
            return dict1
        else:
            buf = open(self.fichier.get_url(), 'rb').read()
            dict2 = ast.literal_eval(re.recognize_by_filebuffer(buf, 0))
            if dict2['status']['msg'] == 'Success' and dict2['metadata'] and dict2['metadata']['music'][0]:
                return dict2


    def update_tag(self,taglist,newtaglist):

        for item in newtaglist.keys():
            for element in taglist:
                if item==element:
                    self.fichier.change_tag(element,newtaglist[item])

    def update_arc(self):
        tag = ['artists', 'album', 'title', 'genres']
        values = self.musique_tag()
        if values:
            c = values['metadata']['music'][0]
            for element in tag:
                try:
                    tagvalue = c[element]
                    liste1 = []
                    if type(tagvalue) is list:
                        for item in tagvalue:
                            liste1.append(item['name'])
                        newtag='&'.join(liste1)
                        self.fichier.change_tag(element,newtag)
                    elif type(tagvalue) is str:
                        self.fichier.change_tag(element, tagvalue)
                    elif type(tagvalue) is dict:
                        self.fichier.change_tag(element, tagvalue['name'])
                except KeyError:
                    continue