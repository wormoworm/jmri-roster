import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.logging import RichHandler

from src.roster_importer import RosterImporter
from src.roster_watcher import RosterWatcher
from src.roster_database import RosterDatabase

DIRECTORY_ROSTER = os.getenv("DIRECTORY_ROSTER", "/roster")
MONITOR_CHANGES = os.getenv("MONITOR_CHANGES", "True").lower() == "true"
DEBUG = os.getenv("DEBUG", "True").lower() == "true"


def does_file_exist(path):
    return os.path.isfile(path)


if __name__ == "__main__":
    # Housekeeping
    logging.basicConfig(
        level="DEBUG" if DEBUG else "INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(omit_repeated_times=False)],
    )
    importer = RosterImporter()
    RosterDatabase().clear_all_data()
    # First, import the roster from the roster directory. This takes care of any roster changes that may have occurred whilst we were not running
    importer.process_existing_files(DIRECTORY_ROSTER)
    # Only watch for roster changes if specified.
    if MONITOR_CHANGES:
        RosterWatcher(roster_importer=importer).watch(DIRECTORY_ROSTER)
