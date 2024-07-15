

from thumbnail_maker import ThumbnailMakerService

img_list = [
    "https://images.freeimages.com/images/large-previews/56d/peacock-1169961.jpg",
    "https://images.freeimages.com/images/large-previews/bc4/curious-bird-1-1374322.jpg"
]

thmbMaker = ThumbnailMakerService()

thmbMaker.make_thumbnails(img_list)