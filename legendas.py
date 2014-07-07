# -*- coding: latin-1 -*-
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
import traceback
from urllib2 import Request, urlopen, URLError, HTTPError
import shutil

#install wget , requests
base_url = 'http://api.thesubdb.com/?{0}'
#user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'
user_agent = 'SubDB/1.0 (Carpinteiro/0.1; https://github.com/Carpinteiro/Legendas)'
my_path = "/home/carpinteiro/WorkSpace/Python/"
config = 'config.txt'
diretorias = []
ficheiros = []
lista_de_filmes = []
lista_de_legendas = []
lista_de_extensoes = []
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
    
    try:
    	response = urllib2.urlopen(req)
    except HTTPError,e :
    	print 'The server couldn\'t fulfill the request.'
    	print 'Error code: ',e.code, 'Not Found'
    except URLError, e:
    	print 'We failed to reach a server.'
    	print 'Reason: ', e.reason
    else:
    	ext = response.info()['Content-Disposition'].split(".")[1]
	    #print response.info()
	print 'done'
	file = os.path.splitext(filename)[0] + "." + ext

	with open(file, "wb") as fout:
		fout.write(response.read())
		return 1

def check_language(filename):
	params = {'action': 'languages'}
	url = base_url.format(urllib.urlencode(params))
	
	req = urllib2.Request(url)
	req.add_header('User-Agent',user_agent)
	
	response = urllib2.urlopen(req)
	#print response.info()
	file = open(filename,"wb")
	file.write("Linguagens disponiveis para download:\n")
	file.write(response.read())

def find_file_extension(filename):
	return os.path.isfile(filename)

#dada uma lista e uma linguagem tenta sacar as legendas
def do_download(List_with_no_subtitle,languageinc):
        for need in List_with_no_subtitle:
        	c = need[:-4]
        	print c
        	c += '.srt'
        	print c
        	print need
        	download_subtitle(get_hash(need),languageinc,c)
        	'''#MP4
        	b = need +'.mp4'
        	result = find_file_extension(b)
        	if result == True:
        		c = need +'.srt'
        		download_subtitle(get_hash(b),languageinc,c)
        	
        	#MKV
        	b = need +'.mkv'
        	print b
        	result = find_file_extension(b)
        	print result
        	if result == True:
        		c = need +'.srt'
        		print c
        		download_subtitle(get_hash(b),languageinc,c)
        	
        	#AVI
        	b = need +'.avi'
        	result = find_file_extension(b)
        	if result == True:
        		c = need +'.srt'
        		download_subtitle(get_hash(b),languageinc,c)'''


#devolve uma lista com todos os filmes sem legenda e guarda as diretorias encontradas
def get_all_files(diretoriaSearch):
	diretoria = os.listdir(diretoriaSearch)
        for file in diretoria:
        	#se for uma pasta
        	if(os.path.isdir(file)):
        		diretorias.append(file)
        	#se for um ficheiro
        	else:
        		ficheiros.append(file)

        print"\nFicheiros:"
        for f in ficheiros:
        	ext = f.split(".")
        	#sem_ext e a extensao
        	sem_ext = ext.pop(len(ext)-1)
        	#nf é o nome do ficheiro sem extensao
        	nf = f[:-4]
        	#print sem_ext
        	if(sem_ext == 'mkv' or sem_ext == 'mp4' or sem_ext == 'avi'):
        		check = nf + '.srt'
        		print "Check"
        		print(check)
        		if not (find_file_extension(check)):
        			lista_de_filmes.append(f)

        	'''elif(sem_ext == 'srt'):
        		lista_de_legendas.append(nf)
       	#list(set(l) - set(l2))
       	#lista de filmes naquela directoria sem .srt
    	nova = list(set(lista_de_filmes) - set(lista_de_legendas))
    	#print lista_de_extensoes'''
    	return lista_de_filmes


def main(argv):
    if len(sys.argv) != 1:
        print "Usage: python legendas.py"
        sys.exit (1)
    else:
        check_language(config)
        print "All information you need is in config.txt"
        print "\nWhat languages do you want to your subtitles?"
        print "if more than one write it like : 'pt,en'\n"
        #languages_choosen = raw_input("I want subtitles in :")

        print "Lista de filmes sem legenda:\n"
        x = get_all_files(my_path)
        print x
        print '\n'
        raw_input("\nPress Enter to download subtitles to those movies...")
        for what in x:
        	leg = what[:-4]
        	legend = leg + '.srt'
        	print "going to write legend here:"
        	print legend
        	print what + "\n"
        	did_it = download_subtitle(get_hash(what),'pt,en',legend)
        	#criar as pastas para cada serie
        	if (did_it == 1):
        		create = my_path + leg
        		print "CREATE"
        		print create
        		os.mkdir( create, 0755 );
        		#move the files
	        	shutil.move(what,create)
	        	shutil.move(legend,create)
        
        for dir in diretorias:
        	#refresh das listas
        	del ficheiros[0:len(ficheiros)]
        	del lista_de_filmes[0:len(lista_de_filmes)]
        	#lista de ficheiros
        	print "LISTA DE FICHEIROS"
        	print ficheiros
        	#criacao da nova diretoria
        	print "NOVA DIR"
        	novadir = my_path + dir
        	print novadir
        	#mudar e verificacao que mudou a diretoria
        	os.chdir(novadir)
        	retval = os.getcwd()
        	print "Directory changed successfully %s" % retval
        	#lista com os filmes a sacar da nova diretoria
        	y = get_all_files(novadir)
        	print "Lista de filmes sem legenda mais abaixo:\n"
        	print y
        	for what in y:
        		leg = what[:-4]
        		legend = leg + '.srt'
        		download_subtitle(get_hash(what),'pt,en',legend)
        	os.chdir(my_path)





        



        

if __name__ == "__main__":
    main(sys.argv[1:])

