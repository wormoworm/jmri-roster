import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.logging import RichHandler

DIRECTORY_ROSTER = os.getenv("DIRECTORY_ROSTER", "/roster")
MONITOR_CHANGES = os.getenv("MONITOR_CHANGES", "True")
DEBUG = os.getenv("DEBUG", "False")


def does_file_exist(path):
    return os.path.isfile(path)


class RosterImporter:
    def process_existing_files(self):
        logging.debug("Scanning for existing files in %s", DIRECTORY_ROSTER)
        for file in os.listdir(DIRECTORY_ROSTER):
            self.process_file(DIRECTORY_ROSTER + "/" + file)

    def process_file(self, input_path):
        # Check the file still exists. The file watcher seems to deliver multiple events per file change, and they seem to all arrive at the same time. So after we have moved the file during the first call to this function, the file will no longer exist.
        if not does_file_exist(input_path):
            return None
        # TODO


class RosterListener(FileSystemEventHandler):

    rosterImporter: RosterImporter

    def __init__(self):
        self.observer = Observer()

    def run(self):
        self.observer.schedule(self, DIRECTORY_ROSTER)
        self.observer.start()
        logging.debug("Listening %s for file changes...", DIRECTORY_ROSTER)
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            logging.debug("Stopping listening...")

        self.observer.join()


if __name__ == "__main__":
    # Housekeeping
    logging.basicConfig(
        level="INFO" if DEBUG else "WARNING",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(omit_repeated_times=False)],
    )
    importer = RosterImporter()
    # First, import the roster from the roster directory. This takes care of any roster changes that may have occurred whilst we were not running
    importer.process_existing_files()
    # Only listen for roster changes if specified.
    if MONITOR_CHANGES == "True":
        RosterListener().run()
