# -*- coding: latin-1 -*-
# to do:
#ir buscar o imdb_id e verificar se a implementação do download que fiz está bem feita
# começar a criar html atraves do id do imdb para ver se bate certp*/

import sys, struct, os
from os import path

from pythonopensubtitles.opensubtitles import OpenSubtitles

opens = OpenSubtitles()
from pythonopensubtitles.utils import File
import base64
import zlib


class Test(object):
    username = 'doctest'
    password = 'doctest'


def first():
    token = opens.login('bad@mail.com', 'badpassword')
    assert token == None
    token = opens.login(Test.username, Test.password)
    assert type(token) == str
    print "Token:\n" + token


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

        for x in range(65536 / bytesize):
            buffer = f.read(bytesize)
            (l_value,) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF  #to remain as 64bit number

        f.seek(max(0, filesize - 65536), 0)
        for x in range(65536 / bytesize):
            buffer = f.read(bytesize)
            (l_value,) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash = "%016x" % hash
        assert type(returnedhash) == str
        return returnedhash

    except(IOError):
        return "IOError"


def searchSubtitlesToImdbId(size, videoHash, Language):
    #data = opens.search_subtitles([{'sublanguageid': Language, 'moviehash': videoHash, 'moviebytesize': size}])
    #data = opens.search_subtitles([{'query': 'South Park', 'season': 1, 'episode': 1,'sublanguageid': 'por'}])
    data = opens.search_subtitles([{'sublanguageid': Language, 'moviehash': videoHash, 'moviebytesize': size}])
    #print "ola"
    #print data[0]
    imdb_id = int(data[0].get('IDMovieImdb'))
    #id_sub = int(data[0].get('IDSubtitleFile'))
    assert type(imdb_id) == int
    #print imdb_id
    return imdb_id


def searchSubtitlesToIDSubtitle(size, videoHash, Language):
    data = opens.search_subtitles([{'sublanguageid': Language, 'moviehash': videoHash, 'moviebytesize': size}])
    id_sub = int(data[0].get('IDSubtitleFile'))
    #print "ID da legenda", id_sub
    return id_sub


def videoSize(name):
    size = os.path.getsize(name)
    #assert type(size) == str
    #assert long(size)
    return size

def downloadSubtitle(idLegenda):
    data = opens.download_subtitles([idLegenda])
    #print data[0]
    # data [0 ] e data [1] tem a mesma coisa
    return data[0]

def decompressFile():
    str_object1 = open('imageToSave.txt', 'rb').read()
    str_object2 = zlib.decompress(str_object1)
    f = open('my_recovered_log_file.srt', 'wb')
    f.write(str_object2)
    f.close()




def main(argv):
    if len(sys.argv) != 1:
        print "Usage: python legendas.py"
        sys.exit(1)
    else:
        first()
        #print "HashFile:"+hashFile('breakdance.avi')
        #print "VideoSize:",videoSize('breakdance.avi')
        a = hashFile('Live.Free.Or.Die.Hard[2007]DvDrip-aXXo.avi')
        b = videoSize('Live.Free.Or.Die.Hard[2007]DvDrip-aXXo.avi')
        #print"ID do Imdb:",(searchSubtitlesToImdbId(b, a, 'por'))
        #print"ID da legenda:",(searchSubtitlesToIDSubtitle(b, a, 'por'))
        c = (searchSubtitlesToIDSubtitle(b, a, 'por'))
        x = downloadSubtitle(c)
        print (x)
        print "Value : %s" %  x.get('data')
        enconde = x.get('data')
        #$print enconde
        stringDecoded = base64.decodestring(enconde)
        #print "StringDecoded:",stringDecoded

        fh = open('imageToSave.txt', 'wb')
        fh.write(stringDecoded)
        fh.close()

        decompressFile()






if __name__ == "__main__":
    main(sys.argv[1:])