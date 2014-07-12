# -*- coding: latin-1 -*-
import os.path
import hashlib
import sys
import urllib2
import requests
import urllib
import urllib2
import glob
import json
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
my_path = ""
languages_choosen = ""
create = ""
#my_path = "/home/carpinteiro/WorkSpace/Python/"
config = {}
#config = 'config.txt'
linguagens = 'linguagens.txt'
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
    	return 0
    except URLError, e:
    	print 'We failed to reach a server.'
    	print 'Reason: ', e.reason
    	return 0
    else:
    	#print response.info()
    	ext = response.info()['Content-Disposition'].split(".")[1]
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

def read_path():
	return config['diretoria']

def read_languages():
    return config['linguagens']

def do_list_download(ListToDownload):
	global create
	#print "List to Download"
	#print ListToDownload
	#raw_input("\nPress Enter to continue...")
	for what in ListToDownload:
		print '\n'+ what
		leg = what[:-4]
		legend = leg + '.srt'
		did = download_subtitle(get_hash(what),languages_choosen,legend)
		if did == 0:
			ListToDownload.remove(what)
			do_list_download(ListToDownload)
			break
		else:
			create = my_path + leg
        	if not os.path.exists(create):
        		#print ListToDownload
        		os.mkdir(create)
        		#move the files
        		shutil.move(what,create)
        		shutil.move(legend,create)
        		ListToDownload.remove(what)
        		do_list_download(ListToDownload)
        		break
        	else:
        		print ""

	
def do_recursive_downloads():
	print diretorias
	if len(diretorias) == 0:
		return
	for dire in diretorias:
		del ficheiros[0:len(ficheiros)]
    	del lista_de_filmes[0:len(lista_de_filmes)]
    	#print "NOVA DIR"
    	novadir = my_path + dire
    	#print novadir
    	#mudar e verificacao que mudou a diretoria
    	os.chdir(novadir)
    	retval = os.getcwd()
    	#print "Directory changed successfully %s" % retval
    	#lista com os filmes a sacar da nova diretoria
    	y = get_all_files(retval)
    	#print "\nLista de filmes sem legenda mais abaixo:\n"
    	#print y
    	do_list_download(y)
    	diretorias.remove(dire)
    	do_recursive_downloads()
    	#break
    	#print my_path
    	#os.chdir(my_path)

#devolve uma lista com todos os filmes sem legenda e guarda as diretorias encontradas
def get_all_files(diretoriaSearch):
	diretoria = os.listdir(diretoriaSearch)
	#print diretoria
        for file in diretoria:
        	if(os.path.isdir(file) and file != "Series"):
        		diretorias.append(file)
        	#se for um ficheiro
        	else:
        		ficheiros.append(file)

        
        for f in ficheiros:
        	ext = f.split(".")
        	#sem_ext e a extensao
        	sem_ext = ext.pop(len(ext)-1)
        	#nf é o nome do ficheiro sem extensao
        	nf = f[:-4]
        	#print sem_ext
        	if(sem_ext == 'mkv' or sem_ext == 'mp4' or sem_ext == 'avi'):
        		check = nf + '.srt'
        		if not (find_file_extension(check)):
        			#print nf
        			lista_de_filmes.append(f)
    	return lista_de_filmes


def main(argv):
    if len(sys.argv) != 1:
        print "Usage: python legendas.py"
        sys.exit (1)
    else:
    	global my_path
        global languages_choosen
       	with open('config.json') as handle:
    		config.update(json.load(handle))
    	#print config["diretoria"]
    	my_path = read_path()
        languages_choosen = read_languages()
        
    	check_language(linguagens)
        print "All information you need is in config.txt"
        print "\nWhat languages do you want to your subtitles?"
        print "if more than one write it like : 'pt,en'\n"
        #languages_choosen = raw_input("I want subtitles in :")

        print "\nLista de filmes sem legenda:\n"
        x = get_all_files(my_path)
        print x
        print '\n'
        raw_input("\nPress Enter to download subtitles to those movies...")
        
        do_list_download(x)
        raw_input("\nPress Enter to download other diretories...")
        do_recursive_downloads()
        #Voltar à pasta inicial
        	
        


if __name__ == "__main__":
    main(sys.argv[1:])

