

class Selectfile():

    def __init__(self,filelist):

        self.filelist=filelist

    def bysize(self,min,max):
        finallist=[]
        for element in self.filelist:
            if element.get_tag('size')>min and element.get_tag('size')<max:
                finallist.append(element)
        return finallist

    def byattribute(self,attribute,value):
        finallist=[]
        for element in self.filelist:
            if element.get_tag(attribute)==value:
                finallist.append(element)
        return finallist

    def byname(self):

        return
    
    def doublon(self):
        listedoublon = []
        for element in self.filelist:
            for element1 in self.filelist:
                if element.get_url() != element1.get_url():
                    if element.get_extension() == element1.get_extension():
                        if element.get_tag('size') == element1.get_tag('size'):
                            with open(element.get_url(), 'rb') as text1:
                                value1 = text1.read(20)
                            with open(element.get_url(), 'rb') as text2:
                                value2 = text2.read(20)
                            if value1 == value2:
                                if element.issame(element1.get_url()):
                                    listedoublon.append(element1)
                                    self.filelist.remove(element1)
            if element in self.filelist:
                self.filelist.remove(element)
        return listedoublon