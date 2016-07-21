# multiline imports for god sake !
import requests,ast,json,xmltodict
from acrcloud.recognizer import ACRCloudRecognizer


class Devine:

    def __init__(self, megafile):
        """
        :param: me
        """
        self.megafile = megafile

    def book_tag(self, param):

        livre = 'https://www.goodreads.com/search.xml?key=bIlqMcaq64Bw2zLbZmYDXQ&q='
        link = livre+param
        dic = ast.literal_eval(json.dumps(xmltodict.parse(requests.get(link).text)))
        result = []
        for item in dic['GoodreadsResponse']['search']['results']['work']:
            result.append((item['best_book']['title'], item['best_book']['author']['name']))
        return result
    
    # todo: use json.load instead of ast.literal_eval
    def movie_tag(self, t=None, y=None):
        # :args t = title, y=year:
        link = r'http://www.omdbapi.com/?'
        # y = y or ''
        if not y:
            y = ''
        # t = t or ''
        if not t:
            t = ''
        # use string.format() instead of '+' concatenation
        link = link + '&t=' + t + '&y=' + y
        dic1 = ast.literal_eval(requests.get(link).text)
        if dic1['Response'] == 'True':
            return dic1

        else:
            t = self.megafile.get_tag('title')
            if t:
                link = link + '&t=' + ''.join(t) + '&y=' + y
                dic2 = ast.literal_eval(requests.get(link).text)
                if dic2['Response'] == 'True':
                    return dic2
                else:
                    t = self.megafile.get_name().split('.')[0:-1]
                    link = link + '&t=' + ''.join(t) + '&y=' + y
                    dic3 = ast.literal_eval(requests.get(link).text)
                    if dic3['Response'] == 'False':
                        return dic3

    def music_print(self):

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
        dict1 = ast.literal_eval(re.recognize_by_file(self.megafile.get_url(), 0))

        if dict1['status']['msg'] == 'Success' and dict1['metadata'] and dict1['metadata']['music'][0]:
            return dict1
        else:
            # make sure to catch IOError
            buf = open(self.megafile.get_url(), 'rb').read()
            dict2 = ast.literal_eval(re.recognize_by_filebuffer(buf, 0))
            if dict2['status']['msg'] == 'Success' and dict2['metadata'] and dict2['metadata']['music'][0]:
                return dict2

    def update_tag(self, dic, genre):

        if genre == 'music_print':
            """tag:'artists', 'album', 'title', 'genres'"""
            try:
                c = dic['metadata']['music'][0]
            except KeyError:
                return None
            for element in dic:
                try:
                    tagvalue = c[element]
                    liste1 = []
                    if type(tagvalue) is list:
                        for item in tagvalue:
                            liste1.append(item['name'])
                        newtag = '&'.join(liste1)
                        self.megafile.change_tag(element, newtag)
                    elif type(tagvalue) is str:
                        self.megafile.change_tag(element, tagvalue)
                    elif type(tagvalue) is dict:
                        self.megafile.change_tag(element, tagvalue['name'])
                except KeyError:
                    continue

        elif genre == 'movie':
            if 'Genre' in dic.keys():
                self.megafile.change_tag('genre',dic['Genre'])
            if 'Title' in dic.keys():
                self.megafile.change_tag('title',dic['Title'])
            if 'Plot' in dic.keys():
                print(dic['Plot'])
            if 'Writer' in dic.keys():
                print(dic['Writer'])
