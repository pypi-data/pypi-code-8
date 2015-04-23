__title__ = 'NameParser'
__version__ = '0.1'
__author__ = 'Ali GOREN <goren.ali@yandex.com>'
__repo__ = 'https://github.com/aligoren/NameParser'
__license__ = 'Apache v2.0 License'

class NameParser:

    def __init__(self):
        self.getName

    def getName(self, name):
        listy = [] # where the needed output is put in
        splitName = name.split(' ')
        
        for i in range(len(splitName)):
            if i==(len(splitName)-1):#when the last word is reach
                listy.append('Surname: '+ splitName[i])
            else:
              listy.append('Name: '+ splitName[i])

        name = '\n'.join(listy)
        return name


nr = NameParser()

print(nr.getName('oguz ali bircan'))


