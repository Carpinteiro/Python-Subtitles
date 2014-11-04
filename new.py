#to do:
	#ir buscar o imdb_id e verificar se a implementação do download que fiz está bem feita
	# começar a criar html atraves do id do imdb para ver se bate certp


import sys,struct,os
from os import path

from pythonopensubtitles.opensubtitles import OpenSubtitles
opens = OpenSubtitles()

from pythonopensubtitles.utils import File

class Test(object):
	username='doctest'
	password='doctest'

def first():
	token = opens.login('bad@mail.com', 'badpassword')
	assert token == None
	token = opens.login(Test.username, Test.password)
	assert type(token) == str
	print "Token:\n"+token

def hashFile(name): 
      try: 
                 
                longlongformat = 'q'  # long long 
                bytesize = struct.calcsize(longlongformat) 
                    
                f = open(name, "rb") 
                    
                filesize = os.path.getsize(name)
                #cast para String para passar como parametro depois
                #assert type(filesize) == str
                assert long(filesize)
                #print filesize

                hash = filesize
                    
                if filesize < 65536 * 2: 
                       return "SizeError" 
                 
                for x in range(65536/bytesize): 
                        buffer = f.read(bytesize) 
                        (l_value,)= struct.unpack(longlongformat, buffer)  
                        hash += 	l_value 
                        hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number  
                         
    
                f.seek(max(0,filesize-65536),0) 
                for x in range(65536/bytesize): 
                        buffer = f.read(bytesize) 
                        (l_value,)= struct.unpack(longlongformat, buffer)  
                        hash += l_value 
                        hash = hash & 0xFFFFFFFFFFFFFFFF 
                 
                f.close() 
                returnedhash =  "%016x" % hash
                assert type(returnedhash) == str
                return returnedhash 
    
      except(IOError): 
                return "IOError"

def searchSubtitles(size,videoHash,Language):
	#data = opens.search_subtitles([{'sublanguageid': Language, 'moviehash': videoHash, 'moviebytesize': size}])
	#data = opens.search_subtitles([{'query': 'South Park', 'season': 1, 'episode': 1,'sublanguageid': 'por'}])
	data = opens.search_subtitles([{'sublanguageid':Language,'moviehash': videoHash, 'moviebytesize': size}])
	print "ola"
	print data[0]
	imdb_id = int(data[0].get('IDMovieImdb'))
	id_sub = int(data[0].get('IDSubtitleFile'))
	print "ID da legenda",id_sub
	assert type(imdb_id) == int
	print imdb_id

def videoSize(name):
	size = os.path.getsize(name)
	#assert type(size) == str
	#assert long(size)
	return size

def download(id):
	print "por fazer"





	



def main(argv):
    if len(sys.argv) != 1:
        print "Usage: python legendas.py"
        sys.exit (1)
    else:
    	first()
    	#print "HashFile:"+hashFile('breakdance.avi')
    	#print "VideoSize:",videoSize('breakdance.avi')
    	a = hashFile('Live.Free.Or.Die.Hard[2007]DvDrip-aXXo.avi')
    	b = videoSize('Live.Free.Or.Die.Hard[2007]DvDrip-aXXo.avi')
    	searchSubtitles(b,a,'por')
    	


if __name__ == "__main__":
	main(sys.argv[1:])