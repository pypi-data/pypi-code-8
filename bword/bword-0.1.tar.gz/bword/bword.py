# -*-coding:utf8-*-
import json
import requests
import sys
import getopt

APIKEY = 'MzzkcoZZwoGRM0bDjSr54tkA'

red = '\033[31;1m %s \033[1;m'
green = '\033[32;1m %s \033[1;m'
yellow = '\033[33;1m %s \033[1;m'
blue = '\033[34;1m %s \033[1;m'
ultramarine = '\033[36;1m %s \033[1;m'

def usage():
     return """Usage: python %s 
            [-h|--help] for help 
            [[-s||--source] world] for translate  """ %sys.argv[0] 

def translate(args=None):
    global APIKEY
    if args == None:
        URL = "http://openapi.baidu.com/public/2.0/translate/dict/simple?client_id=%s&q=%s&from=en&to=zh" % (APIKEY, sys.argv[2])
        word= sys.argv[2]
    else:
        URL = "http://openapi.baidu.com/public/2.0/translate/dict/simple?client_id=%s&q=%s&from=en&to=zh" % (APIKEY, args)     
        word = args
    rawjson = requests.get(URL).text
    decodejson = json.loads(rawjson)
    first = decodejson['data']['symbols'][0]['parts']
    print blue %'英文: ' + ultramarine % word
    print blue % '简明释义: '
    for x in first:
        print blue % x['part'], yellow % (';'.join(x['means']).encode('utf8'))
    return ''

def main():
    opts, args = getopt.getopt(sys.argv[1:], 'hs:', ["help","source:" ])
    if len(args) == 1:
        print translate(args[0])
    else:
        for opt, args in opts:
            if not opt:
                print usage()
            if opt in ('-h', '--help'):
                print usage()
            if opt in ('-s', '--source'):
                print translate()

if __name__ == '__main__':
    main()