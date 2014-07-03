import os.path
import hashlib
import wget
import sys
import urllib2
import requests
import urllib
import urllib2
import glob
from os import listdir
from os.path import isfile, join

#install wget , requests
base_url = 'http://api.thesubdb.com/?{0}'
#user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'
user_agent = 'SubDB/1.0 (Carpinteiro/0.1; https://github.com/Carpinteiro/Legendas)'
my_path = "/home/carpinteiro/WorkSpace/Python/"
config = 'config.txt'
diretorias = []
ficheiros = []

#verificar se o ficheiro existe
'''if not os.path.isfile(HASHES_FILE):
        logger.info("hash file does not exist yet")
        return'''

#this hash function receives the name of the file and returns the hash code
def get_hash(name):
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            size = os.path.getsize(name)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

# executa o download usando a biblioteca
def download_subtitle(hashinc,languageinc,filename):
    params = {'action': 'download', 'language': languageinc, 'hash': hashinc}
    url = base_url.format(urllib.urlencode(params))
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    
    response = urllib2.urlopen(req)
    ext = response.info()['Content-Disposition'].split(".")[1]
    print response.info()
    file = os.path.splitext(filename)[0] + "." + ext

    with open(file, "wb") as fout:        
        fout.write(response.read())

    #url = 'http://api.thesubdb.com/?action=download&hash=' + hashinc + '&language='+languageinc
    #print url
    #wget.download(url)

def check_language(filename):
	params = {'action': 'languages'}
	url = base_url.format(urllib.urlencode(params))
	
	req = urllib2.Request(url)
	req.add_header('User-Agent',user_agent)
	
	response = urllib2.urlopen(req)
	print response.info()
	file = open(filename,"wb")
	file.write(response.read())


def have_subtitle(filename,diretoriaSearch):
	diretoria = os.listdir(diretoriaSearch)
	ext = filename.split(".")
	contem = ext.pop(len(ext)-1)
	print contem
	#print(ext.index(len(ext)-1))
	
def get_all_files(diretoriaSearch):
	diretoria = os.listdir(diretoriaSearch)
        for file in diretoria:
        	if(os.path.isdir(file)):
        		diretorias.append(file)
        		#print "TEM UM"
        	else:
        		ficheiros.append(file)
        		#print file
        for f in ficheiros:
        	have_subtitle(f,diretoriaSearch)
        	print f


def main(argv):
    if len(sys.argv) != 1:
        print "Usage: python legendas.py"
        sys.exit (1)
    else:
        #download_subtitle(get_hash('Californication.S07E05.720p.HDTV.x264-2HD.mkv'),'pt,en','Californication.S07E05.720p.HDTV.x264-2HD.srt')
        #print glob.glob("/home/carpinteiro/WorkSpace/Python/*")
        onlyfiles = [ f for f in listdir(my_path) if isfile(join(my_path,f)) ]
        print onlyfiles

        check_language(config)
        get_all_files(my_path)


        

if __name__ == "__main__":
    main(sys.argv[1:])

