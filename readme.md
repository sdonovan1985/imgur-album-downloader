# imgur Gallery Downloader

This is a simple Python script that contains a class and command line interface that
allows you to download ann images at full resolution in an imgur gallery, all at once.

This is based off of the Imgur Album Downloader from Alex Gisby (https://github.com/alexgisby/imgur-album-downloader) and works with galleries only. 

## Requirements

Python > 2.6

## Command Line Usage

	$ python imgurgallery.py [gallery URL] [folder to save to]

Download all images from an gallery into the folder /Users/alex/images/downloaded

	$ python imgurgallery.py http://imgur.com/gallery/2WlYLZr /Users/alex/images/downloaded
	
Downloads all images and puts them into an gallery in the current directory called "2WlYLZr"

	$ python imgurgallery.py http://imgur.com/gallery/2WlYLZr


## Class Usage

The class allows you to download imgur gallery in your own Python programs without going
through the command line. Here's an example of it's usage:

### Example:
	downloader = ImgurGalleryDownloader("http://imgur.com/gallery/2WlYLZr")
	print "This albums has %d images" % downloader.num_images()
	downloader.save_images()

### Callbacks:
You can hook into the classes process through a couple of callbacks:
	
	downloader.on_image_download()
	downloader.on_complete()

You can see what params and such your callback functions get by looking at the docblocks
for the on_XXX functions in the .py file.

## Full docs:

The whole shebang, class and CLI is fully documented using string-docblock things in the single .py file
so please read through that rather than rely on this readme which could drift out of date.

## License

MIT

## Credits

Written by [Alex Gisby](https://github.com/alexgisby) ([@alexgisby](http://twitter.com/alexgisby))

With [Contributions](https://github.com/alexgisby/imgur-album-downloader/graphs/contributors) from:

- [Lemuel Formacil](https://github.com/lemuelf)
- [Vikraman Choudhury](https://github.com/vikraman)

# Modifications
Modified for Gallery useage by [Sean Donovan](https://github.com/sdonovan1985).

In addition to the gallery modifications, there is also a scraper that looks through a copy of 
Imgur's homepage. This is in the file imgurscraper.py.

Requires code from [entropy-calculation](https://github.com/sdonovan1985/entropy-calculation)
to fully function. imgurscraper.py will not run without this code, which is not included.

