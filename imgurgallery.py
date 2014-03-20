#!/usr/bin/env python
# encoding: utf-8
"""
imgurgallery.py - Download a whole imgur gallery in one go.
Based on https://github.com/alexgisby/imgur-album-downloader

Provides both a class and a command line utility in a single script
to download Imgur gallery.

MIT License
Copyright Alex Gisby <alex@solution10.com>
Copyright Sean Donovan <sdonovan@cc.gatech.edu>
"""

import sys
import re
import urllib
import os
import math

help_message = '''
Quickly and easily download a gallery from Imgur.

Format:
    $ python imgurgallery.py [gallery URL] [destination folder]

Example:
    $ python imgurgallery.py http://imgur.com/gallery/2WlYLZr /Users/alex/images

If you omit the dest folder name, the utility will create one with the same name as the
gallery (for example for http://imgur.com/gallery/uOOju it'll create uOOju/ in the cwd)

'''

class ImgurGalleryException(Exception):
    def __init__(self, msg=False):
        self.msg = msg


class ImgurGalleryDownloader:
    def __init__(self, gallery_url):
        """
        Constructor. Pass in the gallery_url that you want to download.
        """
        self.gallery_url = gallery_url

        # Callback members:
        self.image_callbacks = []
        self.complete_callbacks = []

        # Check the URL is actually imgur:
        match = re.match('(https?)\:\/\/(www\.)?(?:m\.)?imgur\.com/gallery/([a-zA-Z0-9]+)?', gallery_url)
        if not match:
            raise ImgurGalleryException("URL must be a valid Imgur Gallery")

        self.protocol = match.group(1)
        self.gallery_key = match.group(3)
        print "protocol    - ", self.protocol
        print "gallery key - ", self.gallery_key

        # Read the no-script version of the page for all the images:
        noscriptURL = 'http://imgur.com/gallery/' + self.gallery_key
# + '/noscript'
        self.response = urllib.urlopen(noscriptURL)

        if self.response.getcode() != 200:
            raise ImgurGalleryException("Error reading Imgur: Error Code %d" % self.response.getcode())

        # Read in the images now so we can get stats and stuff:
        html = self.response.read()
        self.images = re.findall('<img src="(\/\/i\.imgur\.com\/([a-zA-Z0-9]+\.(jpg|jpeg|png|gif)))"', html)

    def num_images(self):
        """
        Returns the number of images that are present in this gallery.
        """
        return len(self.images)

    def gallery_key(self):
        """
        Returns the key of this gallery. Helpful if you plan on generating your own
        folder names.
        """
        return self.gallery_key

    def on_image_download(self, callback):
        """
        Allows you to bind a function that will be called just before an image is
        about to be downloaded. You'll be given the 1-indexed position of the image, it's URL 
        and it's destination file in the callback like so:
            my_awesome_callback(1, "http://i.imgur.com/fGWX0.jpg", "~/Downloads/1-fGWX0.jpg")
        """
        self.image_callbacks.append(callback)

    def on_complete(self, callback):
        """
        Allows you to bind onto the end of the process, displaying any lovely messages
        to your users, or carrying on with the rest of the program. Whichever.
        """
        self.complete_callbacks.append(callback)


    def save_images(self, foldername=False):
        """
        Saves the images from the gallery into a folder given by foldername.
        If no foldername is given, it'll use the cwd and the gallery key.
        And if the folder doesn't exist, it'll try and create it.
        """
        # Try and create the gallery folder:
        if foldername:
            galleryFolder = foldername
        else:
            galleryFolder = self.gallery_key

        if not os.path.exists(galleryFolder):
            os.makedirs(galleryFolder)

        # And finally loop through and save the images:
        for (counter, image) in enumerate(self.images, start=1):
            image_url = "%s:%s" % (self.protocol, image[0])

            # Fetch hi-res images (Fixes https://github.com/alexgisby/imgur-album-downloader/issues/5)
            image_url = re.sub(r'([a-zA-Z0-9]+)(h)\.(jpg|jpeg|png|gif)$', r'\1.\3', image_url)

            prefix = "%0*d-" % (
                int(math.ceil(math.log(len(self.images) + 1, 10))),
                counter
            )
            path = os.path.join(galleryFolder, prefix + image[1])

            # Run the callbacks:
            for fn in self.image_callbacks:
                fn(counter, image_url, path)

            # Actually download the thing
            urllib.urlretrieve(image_url, path)

        # Run the complete callbacks:
        for fn in self.complete_callbacks:
            fn()


if __name__ == '__main__':
    args = sys.argv

    if len(args) == 1:
        # Print out the help message and exit:
        print help_message
        exit()

    try:
        # Fire up the class:
        downloader = ImgurGalleryDownloader(args[1])
        print "Found %d images in gallery" % downloader.num_images()

        # Called when an image is about to download:
        def print_image_progress(index, url, dest):
            print "Downloading Image %d" % index
            print "    %s >> %s" % (url, dest)
        downloader.on_image_download(print_image_progress)

        # Called when the downloads are all done.
        def all_done():
            print ""
            print "Done!"
        downloader.on_complete(all_done)

        # Work out if we have a foldername or not:
        if len(args) == 3:
            galleryFolder = args[2]
        else:
            gallleryFolder = False

        # Enough talk, let's save!
        downloader.save_images(galleryFolder)
        exit()

    except ImgurGalleryException as e:
        print "Error: " + e.msg
        print ""
        print "How to use"
        print "============="
        print help_message
        exit(1)
