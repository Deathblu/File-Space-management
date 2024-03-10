
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

source_dir = "C:/Users/anuwa/Downloads"

# Watchdog lib for spotting changes 
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# folders to save in
dest_sfx="C:/Users/anuwa/Downloads/SFX"
dest_soft="C:/Users/anuwa/Downloads/Software"
dest_music="C:/Users/anuwa/Downloads/Music"
dest_videos="C:/Users/anuwa/Downloads/Videos"
dest_images="C:/Users/anuwa/Downloads/Images"
dest_docs="C:/Users/anuwa/Downloads/Docs"

# images extensions
image_ext = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

audio_ext = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]   

video_ext = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

doc_ext = [".doc", ".docx", ".odt",".pdf", ".xls", ".xlsx", ".ppt", ".pptx",".txt"]

soft_ext = [".torrent",".exe",".zip",".msi"]
# to handle duplicate files by making them unique
def make_unique(dest,name):
    filename,extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
        
    return name


def move_file(dest,entry,name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest,name)
        oldName = join(dest,name)
        newName = join(dest,unique_name)
        rename(oldName,newName)
    move(entry, dest)
    
    
class MoverHandler(FileSystemEventHandler):
    def on_modified(self,event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry,name)
                self.check_video_files(entry,name)
                self.check_image_files(entry,name)
                self.check_document_files(entry,name)
                self.check_software_files(entry,name)

    def check_audio_files(self, entry, name):  # * Checks all Audio Files
        for audio_extension in audio_ext:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:  # ? 10Megabytes
                    dest = dest_sfx
                else:
                    dest = dest_music
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_ext:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_videos, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_ext:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_images, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in doc_ext:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_docs, entry, name)
                logging.info(f"Moved document file: {name}")            
    
    def check_software_files(self, entry, name):  # * Checks all Audio Files
        for software_extension in soft_ext:
            if name.endswith(software_extension) or name.endswith(software_extension.upper()):
                move_file(dest_soft, entry, name)
                logging.info(f"Moved software file: {name}")    


# watchdog code
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()  