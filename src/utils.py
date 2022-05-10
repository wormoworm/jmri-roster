import os
from os.path import exists

DIRECTORY_ROSTER = os.getenv("DIRECTORY_ROSTER", "/roster")
IMAGE_FILE_EXTENSIONS = [ ".jpg", ".jpeg", ".png"]

ROSTER_DATABASE_LOCATION = os.getenv("ROSTER_DATABASE_LOCATION", "/data/roster.db")
os.makedirs(os.path.dirname(ROSTER_DATABASE_LOCATION), exist_ok=True)

def search_for_roster_entry_image(roster_id: str) -> str:
    for file in os.listdir(DIRECTORY_ROSTER):
        file_path = f"{DIRECTORY_ROSTER}/{file}"
        filename, file_extension = os.path.splitext(file_path)
        if filename.endswith(roster_id) and file_extension.lower() in IMAGE_FILE_EXTENSIONS:
            return file_path
    return None