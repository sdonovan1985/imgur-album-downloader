import re
import urllib2
import os
from imgurgallery import *
from entropycalc import *


def downloadimgur(source):
    f = open(source, 'r')

#<img src="//i.imgur.com/yUdo3SMb.jpg" width="48" height="48" />
#    imglink = re.compile('\s*<img src="//i.imgur.com/[a-zA-Z0-9]+
    count = 0
    for line in f:
#        if "width=\"48\" height=\"48\"" in line:
        if "class=\"post\"" in line:
            count += 1
            print count , " - " ,line
            parts = line.split("\"")
            #print parts[1]
#http://i.imgur.com/HVvuwqa.jpg
            imglink = "http://i.imgur.com/" + parts[1] + ".jpg"
            print imglink
            img = urllib2.urlopen(imglink)
#            https://stackoverflow.com/questions/4028697/how-do-i-download-a-zip-file-in-python-using-urllib2
            with open("imgs/"+parts[1]+".jpg", "wb") as local_file:
                local_file.write(img.read())
            

def getGalleries(source):
    f = open(source, 'r')
    galleries = []
    count = 0
    for line in f:
        if "class=\"post\"" in line:
            count += 1
            parts = line.split("\"")
            gallink = "http://imgur.com/gallery/" + parts[1]
            galleries.append(gallink)
            print count, " - ", gallink
    return galleries

def downloadGalleries(galleries, dest):
    for gal in galleries:
        downloader = ImgurGalleryDownloader(gal)
        print "This gallery has %d images" % downloader.num_images()
        downloader.save_images(dest)

def downloadAndEntropyGalleries(galleries, dest):
    for gal in galleries:
        downloader = ImgurGalleryDownloader(gal)
        downloader.on_image_download(appendToCSV)
        print "This gallery has %d images" % downloader.num_images()
        downloader.save_images(dest)


def appendToCSV(count, url, filename):
    #only care about the filename, the rest ignore
    entropy = entropy_of_file(filename)
    filesize = os.stat(filename).st_size

    #https://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    filetype = os.path.splitext(filename)[1]
    filename = os.path.basename(filename)

    string = filename + ", " + filetype + ", " + str(entropy) + ", " + str(filesize) + "\n"
#    print filename, ", ", filetype, ", ", entropy, ", ", filesize

    with open("testdata.csv", "a") as myfile:
        myfile.write(string)

def scrapeDirectory(directory, outputfile):
    for filename in os.listdir(directory):
        print "scraping " + directory + filename
        entropy_of_file_chunks(directory + filename, 10000, outputfile)

def scrapeDirectoryTotals(directory, outputfile):
    outfile = open(outputfile, "w")
    for filename in os.listdir(directory):
        print "scraping " + directory + filename
        entropy = entropy_of_file(directory + filename)
        filesize = os.stat(directory + filename).st_size
        filetype = os.path.splitext(filename)[1]

        string = filename + ", " + filetype + ", " + str(entropy) + ", " + str(filesize) + ", " + "\n"
        outfile.write(string)
    outfile.close()


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    downloadAndEntropyGalleries(getGalleries(input_file), output_dir)
