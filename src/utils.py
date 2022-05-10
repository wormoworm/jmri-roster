import os
from os.path import exists
import logging

DIRECTORY_ROSTER = os.getenv("DIRECTORY_ROSTER", "/roster")
IMAGE_FILE_EXTENSIONS = [ ".jpg", ".jpeg", ".png"]

ROSTER_DATABASE_LOCATION = os.getenv("ROSTER_DATABASE_LOCATION", "/data/roster.db")
os.makedirs(os.path.dirname(ROSTER_DATABASE_LOCATION), exist_ok=True)

def search_for_roster_entry_image(roster_id: str) -> str:
    logging.info("search_for_roster_entry_image, id = %s", roster_id)
    for file in os.listdir(DIRECTORY_ROSTER):
        logging.info("file in dir: %s", file)
        file_path = f"{DIRECTORY_ROSTER}/{file}"
        logging.info("file path: %s", file_path)
        filename, file_extension = os.path.splitext(file_path)
        logging.info("file name: %s, path: %s", filename, file_extension)
        if filename.endswith(roster_id) and file_extension.lower() in IMAGE_FILE_EXTENSIONS:
            return file_path
    return None