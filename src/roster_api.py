from queue import Empty
from fastapi import FastAPI, HTTPException, Request, Response
import os
from os.path import exists
from io import BytesIO
from PIL import Image
from roster_database import RosterDatabase
from playhouse.shortcuts import model_to_dict
from datetime import datetime
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import StreamingResponse
import logging

DIRECTORY_ROSTER = os.getenv("DIRECTORY_ROSTER", "/roster")
IMAGE_FILE_EXTENSIONS = [ ".jpg", ".jpeg", ".png"]

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/api/v2/roster")
def get_roster():
    entries = RosterDatabase().get_all_roster_entries()
    entries_array = []
    for entry in entries:
        entries_array.append(model_to_dict(entry, backrefs=True))
    return {"roster": entries_array}


@app.get("/api/v2/roster_entry/id/{id}")
def get_roster_entry_by_id(id: str):
    entry = RosterDatabase().get_roster_entry_by_id(id)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Roster entry with id {id} not found")
    return {"roster_entry": model_to_dict(entry, backrefs=True)}


@app.get("/api/v2/roster_entry/address/{address}")
def get_roster_entry_by_address(address: str):
    entry = RosterDatabase().get_roster_entry_by_address(address)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Roster entry with address {address} not found")
    return {"roster_entry": model_to_dict(entry, backrefs=True)}


def output_roster_image(file_path: str, size: int = None) -> Response:
    with Image.open(file_path) as image:
        # Resize image if size is set
        if size:
            width, height = image.size
            # Don't bother resizing if the requested size is greater than or equal to the source image size.
            if size < width:
                aspect_ratio = width / height
                desired_width = size
                desired_height = round(desired_width / aspect_ratio)
                image = image.resize((desired_width, desired_height), Image.ANTIALIAS)
        image_bytes = BytesIO()
        image.save(image_bytes, format="png")
        # media_type here sets the media type of the actual response sent to the client.
        return Response(content=image_bytes.getvalue(), media_type="image/png")


def search_for_roster_entry_image(roster_id: str) -> str:
    for file in os.listdir(DIRECTORY_ROSTER):
        file_path = f"{DIRECTORY_ROSTER}/{file}"
        filename, file_extension = os.path.splitext(file_path)
        if filename.endswith(roster_id) and file_extension.lower() in IMAGE_FILE_EXTENSIONS:
            return file_path
    return None

# TODO: Simplify once new get_image() function added to RosterEntry.
@app.get("/api/v2/roster_entry/{id}/image")
def get_roster_entry_image(id: str, size: int = None, search_files: bool = True):
    entry = RosterDatabase().get_roster_entry_by_id(id)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Roster entry with id {id} not found")
    image_file_path = entry.get_image_file_full_path(search_files)
    if image_file_path:
        try:
            return output_roster_image(f"{DIRECTORY_ROSTER}/{entry.image_file_path}", size)
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=f"Error loading load image for roster entry {id}: {str(e)}.")
    else:
        raise HTTPException(status_code=404, detail=f"Could not find image for roster entry {id}: {str(e)}.")


@app.get("/", response_class=HTMLResponse)
async def show_roster(request: Request):
    entries = RosterDatabase().get_all_roster_entries()
    return templates.TemplateResponse("roster.html", {"request": request, "roster_entries": entries})


@app.get("/roster_entry/{id}", response_class=HTMLResponse)
async def show_roster_entry(request: Request, id: str):
    entry = RosterDatabase().get_roster_entry_by_id(id)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Roster entry with id {id} not found")
    return templates.TemplateResponse("roster_entry.html", {"request": request, "roster_entry": entry})