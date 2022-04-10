import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from importer.roster_importer import RosterImporter

class RosterWatcher(FileSystemEventHandler):

    roster_importer: RosterImporter

    def __init__(self, roster_importer: str):
        self.roster_importer = roster_importer
        self.observer = Observer()

    def watch(self, watch_directory: str):
        self.observer.schedule(self, watch_directory)
        self.observer.start()
        logging.info("Watching %s for roster changes...", os.path.abspath(watch_directory))
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            logging.info("Stopping watching...")

        self.observer.join()
    
    # @staticmethod
    def on_any_event(self, event):
        logging.debug("Received event in input directory: %s", event.event_type)
        if event.is_directory:
            return None

        elif event.event_type == 'modified':
            time.sleep(1)   # This can help avoid processing files that are not yet fully written to disk.
            # logging.info("Modified event")
            self.roster_importer.process_file(event.src_path)