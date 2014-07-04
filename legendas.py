import os.path
import hashlib
import sys
import urllib2
import requests
import urllib
import urllib2
import glob
from os import listdir
from os.path import isfile, join
import collections

#install wget , requests
base_url = 'http://api.thesubdb.com/?{0}'
#user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'
user_agent = 'SubDB/1.0 (Carpinteiro/0.1; https://github.com/Carpinteiro/Legendas)'
my_path = "/home/carpinteiro/WorkSpace/Python/"
config = 'config.txt'
diretorias = []
ficheiros = []
nl = []
nnl = []

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
	file.write("Linguagens disponiveis para download:\n")
	file.write(response.read())

##METODO ESTA NO GET_ALL FILES
def have_subtitle(filename,diretoriaSearch):
	diretoria = os.listdir(diretoriaSearch)
	
	#lista com as extensoes dos ficheiros
	ext = filename.split(".")
	sem_ext = ext.pop(len(ext)-1)
	#print sem_ext

	nf = filename[:-4]
	print nf
	if(sem_ext == 'mkv' or sem_ext == 'srt' or sem_ext == 'mp4'):
	#nome dos ficheiros sem a extensao
		nl.append(nf)
	print("lista")
	print nl
	nova = [x for x, y in collections.Counter(nl).items() if y > 1]
		
	
	

	#sem_ext = ext.pop(len(ext)-1)
	#print sem_ext
	#print(ext.index(len(ext)-1))
def list_duplicates(seq):
  seen = set()
  seen_add = seen.add
  # adds all elements it doesn't know yet to seen and all other to seen_twice
  seen_twice = set( x for x in seq if x in seen or seen_add(x) )
  # turn the set into a list (as requested)
  return list( seen_twice )

def remove_duplicates(l):
    return list(set(l))

def get_all_files(diretoriaSearch):
	diretoria = os.listdir(diretoriaSearch)
        for file in diretoria:
        	if(os.path.isdir(file)):
        		diretorias.append(file)
        		#print "TEM UM"
        	else:
        		ficheiros.append(file)
        		#print file
        print"\nFicheiros:"
        for f in ficheiros:
        	#have_subtitle(f,diretoriaSearch)
        	#print f
        	ext = f.split(".")
        	sem_ext = ext.pop(len(ext)-1)
        	nf = f[:-4]
        	#print nf
        	if(sem_ext == 'mkv' or sem_ext == 'mp4'):
        		nl.append(nf)
        	elif(sem_ext == 'srt'):
        		nnl.append(nf)
       	#list(set(l) - set(l2))
    	print"\nDiretorias:"
    	for p in diretorias:
    		print p
    		#get_all_files(p)
    	#nova = [x for x, y in collections.Counter(nl).items() if x > 0]
    	#print nl
    	#print nnl
    	#seen = set()
    	#seen_add = seen.add
    	#nova = [ x for x in nl if not (x in seen() or seen_add(x))]
    	#nova = remove_duplicates(nl)
    	nova = list(set(nl) - set(nnl))
    	print nova


def main(argv):
    if len(sys.argv) != 1:
        print "Usage: python legendas.py"
        sys.exit (1)
    else:
        #download_subtitle(get_hash('Californication.S07E05.720p.HDTV.x264-2HD.mkv'),'pt,en','Californication.S07E05.720p.HDTV.x264-2HD.srt')
        #download_subtitle(get_hash('Petals.On.The.Wind.2014.HDRip.XviD-EVO.avi'),'pt,en','Petals.On.The.Wind.2014.HDRip.XviD-EVO.srt')
        #download_subtitle(get_hash('Game of Thrones S02E01.mp4'),'pt,en','Game of Thrones S02E01.srt')
        #print glob.glob("/home/carpinteiro/WorkSpace/Python/*")
        #onlyfiles = [ f for f in listdir(my_path) if isfile(join(my_path,f)) ]
        #print onlyfiles

        #check_language(config)
        get_all_files(my_path)


        

if __name__ == "__main__":
    main(sys.argv[1:])

