import time
import os
import logging
from urllib.parse import urlparse
from urllib.request import urlretrieve

import PIL
from PIL import Image
import PIL.Image

import multiprocessing

from queue import Queue, Empty
from threading import Thread

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
        self.img_list= []
               
    def download_image(self, download_queue: Queue):
        while not download_queue.empty():
            try:
                url = download_queue.get(block=False)
                img_filename = urlparse(url).path.split('/')[-1]        
                dest_path = self.input_dir + os.path.sep + img_filename        
                urlretrieve(url, dest_path)        
                self.img_list.append(img_filename)
                
                download_queue.task_done()
            except Queue.Empty:
                logging.info("Queue empty")
               
    # def download_images(self, img_url_list):
    #     if not img_url_list:
    #         return
        
    #     os.makedirs(self.input_dir, exist_ok=True)
        
    #     logging.info("beginning image downloads")
        
    #     start = time.perf_counter()        
        
    #     for url in img_url_list:
    #         img_filename = urlparse(url).path.split('/')[-1]        
    #         dest_path = self.input_dir + os.path.sep + img_filename        
    #         urlretrieve(url, dest_path)        
    #         self.img_queue.put(img_filename)
           
    #     end = time.perf_counter()        
        
    #     # poison pill technique
    #     # tell the queue there is no more message to process
    #     self.img_queue.put(None)        
        
    #     logging.info("downloaded {} images in {} seconds".format(len(img_url_list), end - start))
        
    # def perform_resizing(self):
        
    #     os.makedirs(self.output_dir, exist_ok=True)
        
    #     logging.info("beginning image resizing...")
    #     target_sizes = [32, 64, 200]
    #     num_images = len(os.listdir(self.input_dir))
        
    #     start = time.perf_counter()
    #     while True:
    #         filename = self.img_queue.get()            
    #         # check if the filename is normal or it is a poison pill (None) message
    #         if filename:
            
    #             logging.info("resizing image {}".format(filename))
    #             orig_img = Image.open(self.input_dir + os.path.sep + filename)
    #             for basewidth in target_sizes:
    #                 img = orig_img
    #                 # calculate target height of the resized image to maintain the aspect ratio
    #                 wpercent = (basewidth / float(img.size[0]))
    #                 hsize = int((float(img.size[1]) * float(wpercent)))
    #                 # perform resizing 
    #                 img = img.resize((basewidth, hsize), PIL.Image.Resampling.LANCZOS)
    #                 # save the resize image to the output dir with a modified file name
    #                 new_filename = os.path.splitext(filename)[0] + '_' + str(basewidth) + os.path.splitext(filename)[1]
    #                 img.save(self.output_dir + os.path.sep + new_filename)
                    
    #             os.remove(self.input_dir + os.path.sep + filename)
    #             logging.info("done resizing image {}".format(filename))
    #             self.img_queue.task_done()
                
    #         else:
    #             self.img_queue.task_done()
    #             break
                
    #     end = time.perf_counter()
        
    #     logging.info("created {} thumbnails in {} seconds".format(num_images, end-start))
        
    def resize_image(self, filename):
        target_sizes = [32, 64, 200]
        
        logging.info("resizing image {}".format(filename))
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
        logging.info("done resizing image {}".format(filename))
        
    def make_thumbnails(self, img_url_list):
        logging.info("START make thumbnails")
        pool = multiprocessing.Pool()
        start = time.perf_counter()
        
        download_queue = Queue()
        
        for img_url in img_url_list:
            download_queue.put(img_url)
                        
        num_dl_threads = 4
        for _ in range(num_dl_threads):
            t = Thread(target=self.download_image, args=(download_queue,))
            t.start()
                    
        download_queue.join()

        start_resize = time.perf_counter()
        pool.map(self.resize_image, self.img_list)        
        end_resize = time.perf_counter()
                
        end = time.perf_counter()
        
        pool.close()
        pool.join()
        
        logging.info("created {} thumbnails in {} seconds".format(len(self.img_list), end_resize-start_resize))
        logging.info("END make_thumbnails in {} seconds".format(end-start))
    
executor = ThumbnailMakerService()
executor.make_thumbnails(img_list)