import time
import os
import logging
from urllib.parse import urlparse
from urllib.request import urlretrieve

import threading

import PIL
from PIL import Image
import PIL.Image

# log message format
FORMAT = "[%(threadName)s, %(asctime)s, %(levelname)s] %(message)s"
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format=FORMAT)

img_list = [
    "https://images.freeimages.com/images/large-previews/56d/peacock-1169961.jpg",
    "https://images.freeimages.com/images/large-previews/bc4/curious-bird-1-1374322.jpg",
    "https://images.freeimages.com/images/large-previews/866/butterfly-1-1535829.jpg",
    "https://images.freeimages.com/images/large-previews/ab3/puppy-2-1404644.jpg",
    "https://images.freeimages.com/images/large-previews/39a/spring-1377434.jpg",
    "https://images.freeimages.com/images/large-previews/83f/paris-1213603.jpg"
]

class ThumbnailMakerService(object):
    def __init__(self, home_dir='.'):
        self.home_dir = home_dir
        self.input_dir = self.home_dir + os.path.sep + 'incoming'
        self.output_dir = self.home_dir + os.path.sep + 'outgoing'
        self.downloaded_bytes = 0
        # lock
        self.dl_lock = threading.Lock()
        # semaphore permits
        max_concurrent_dl = 4
        self.dl_sem = threading.Semaphore(max_concurrent_dl)
        
    def download_image(self, url):
        
        # call the semaphore
        self.dl_sem.acquire()
        
        try:
        
            logging.info("downloading image at URL " + url)
            
            # download each image and save to the input dir
            img_filename = urlparse(url).path.split('/')[-1]
            
            dest_path = self.input_dir + os.path.sep + img_filename
            
            urlretrieve(url, dest_path)
            img_size = os.path.getsize(dest_path)
            
            with self.dl_lock: # using with to ensure the lock will automatic acquire and release
                self.downloaded_bytes += img_size
            
            logging.info("image [{} bytes] saved to {}".format(img_size, dest_path))
        
        finally:
            # ensure the release will always being called even there is an exception
            # release semaphore
            self.dl_sem.release()
        
    def download_images(self, img_url_list):
        # validate inputs
        if not img_url_list:
            return
        
        os.makedirs(self.input_dir, exist_ok=True)
        
        logging.info("beginning image downloads")
        
        start = time.perf_counter()
        
        # worker thread list
        threads:list[threading.Thread] = []
        
        for url in img_url_list:
            t = threading.Thread(target=self.download_image, args=(url,))
            t.start()
            threads.append(t)
        
        # join back all the threads
        for t in threads:
            t.join()
            
        end = time.perf_counter()
        
        logging.info("downloaded {} images in {} seconds".format(len(img_url_list), end - start))
        
    def perform_resizing(self):
        # validate inputs
        if not os.listdir(self.input_dir):
            return
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        logging.info("beginning image resizing...")
        target_sizes = [32, 64, 200]
        num_images = len(os.listdir(self.input_dir))
        
        start = time.perf_counter()
        for filename in os.listdir(self.input_dir):
            orig_img = Image.open(self.input_dir + os.path.sep + filename)
            for basewidth in target_sizes:
                img = orig_img
                # calculate target height of the resized image to maintain the aspect ratio
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                # perform resizing 
                img = img.resize((basewidth, hsize), PIL.Image.Resampling.LANCZOS)
                # save the resize image to the output dir with a modified file name
                new_filename = os.path.splitext(filename)[0] + '_' + str(basewidth) + os.path.splitext(filename)[1]
                img.save(self.output_dir + os.path.sep + new_filename)
                
            os.remove(self.input_dir + os.path.sep + filename)
        
        end = time.perf_counter()
        
        logging.info("created {} thumbnails in {} seconds".format(num_images, end-start))
        
    def make_thumbnails(self, img_url_list):
        logging.info("START make thumbnails")
        start = time.perf_counter()
        
        self.download_images(img_url_list)
        self.perform_resizing()
        
        end = time.perf_counter()
        logging.info("END make_thumbnails in {} seconds".format(end-start))
    
executor = ThumbnailMakerService()
executor.make_thumbnails(img_list)