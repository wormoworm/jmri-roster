from queue import Empty
from fastapi import FastAPI, HTTPException, Request, Response
from starlette.datastructures import Headers
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
from peewee import DoesNotExist
from dataclasses import dataclass, fields
import logging

FORMAT_TIMESTAMP_HTTP_HEADER = "%a, %d %b %Y %H:%M:%S"

@dataclass
class FilterParams:
    owner: str = None
    manufacturer: str = None
    model: str = None
    classification: str = None
    decoder: str = None

    def filter_count(self):
        total = 0
        for field in self.__dataclass_fields__:
            if getattr(self, field):
                total+= 1
        return total

    def has_filters(self):
        return self.filter_count() > 0


DIRECTORY_ROSTER = os.getenv("DIRECTORY_ROSTER", "/roster")
IMAGE_FILE_EXTENSIONS = [ ".jpg", ".jpeg", ".png"]

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/api/v2/roster")
def get_roster(owner: str = None, manufacturer: str = None, model: str = None, classification: str = None, decoder: str = None):
    entries = RosterDatabase().get_roster_entries(owner, manufacturer, model, classification, decoder)
    # Transform the list of RosterEntrys to a list of dicts
    roster = list(map(lambda entry: model_to_dict(entry), entries))
    return {"roster": roster}


@app.get("/api/v2/roster_entry/id/{id}")
def get_roster_entry_by_id(id: str):
    try:
        return {"roster_entry": model_to_dict(RosterDatabase().get_roster_entry_by_id(id), backrefs=True)}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Roster entry with id {id} not found")


@app.get("/api/v2/roster_entry/address/{address}")
def get_roster_entry_by_address(address: str):
    try:
        return {"roster_entry": model_to_dict(RosterDatabase().get_roster_entry_by_address(address), backrefs=True)}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Roster entry with address {address} not found")


@app.get("/api/v2/owners")
async def get_owners():
    return {"owners": RosterDatabase().get_owners()}


@app.get("/api/v2/manufacturers")
async def get_manufacturers():
    return {"manufacturers": RosterDatabase().get_manufacturers()}


@app.get("/api/v2/models")
async def get_models():
    return {"models": RosterDatabase().get_models()}


@app.get("/api/v2/classifications")
async def get_classifications():
    return {"classifications": RosterDatabase().get_classifications()}


@app.get("/api/v2/decoders")
async def get_decoders():
    return {"decoders": RosterDatabase().get_decoders()}


def output_roster_image(file_path: str, size: int = None, browser_if_modified_since: str = None) -> Response:
    # Get the image file's modification time - we will use this for caching
    image_modified_time = round(os.path.getmtime(file_path))
    # Check this modification timestamp against the one provided by the browser, if supplied.
    if browser_if_modified_since:
        browser_modified_timestamp = round(datetime.strptime(browser_if_modified_since, FORMAT_TIMESTAMP_HTTP_HEADER).timestamp())
        # The the file's modification time is before or equal to the browser's modification time, this means we do not have a more recent image than the browser, so we can simply return a 304.
        if image_modified_time <= browser_modified_timestamp:
            return Response(None, status_code=304)

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
        modified_header_text = datetime.fromtimestamp(image_modified_time).strftime(FORMAT_TIMESTAMP_HTTP_HEADER)
        # Output the modified timestamp so the browser can keep a record of it for the next request.
        headers = { "Last-Modified": modified_header_text}
        # media_type here sets the media type of the actual response sent to the client.
        return Response(content=image_bytes.getvalue(), media_type="image/png", headers=headers)


def search_for_roster_entry_image(roster_id: str) -> str:
    for file in os.listdir(DIRECTORY_ROSTER):
        file_path = f"{DIRECTORY_ROSTER}/{file}"
        filename, file_extension = os.path.splitext(file_path)
        if filename.endswith(roster_id) and file_extension.lower() in IMAGE_FILE_EXTENSIONS:
            return file_path
    return None


@app.get("/api/v2/roster_entry/{id}/image")
def get_roster_entry_image(request: Request, id: str, size: int = None, search_files: bool = True):
    entry = RosterDatabase().get_roster_entry_by_id(id)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Roster entry with id {id} not found")
    image_file_full_path = entry.get_image_file_full_path(search_files)
    if image_file_full_path:
        try:
            return output_roster_image(image_file_full_path, size, request.headers.get("If-Modified-Since"))
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=f"Error loading load image for roster entry {id}: {str(e)}.")
    else:
        raise HTTPException(status_code=404, detail=f"Could not find image for roster entry {id}.")


@app.get("/", response_class=HTMLResponse)
async def show_roster(request: Request, owner: str = None, manufacturer: str = None, model: str = None, classification: str = None, decoder: str = None):
    entries = RosterDatabase().get_roster_entries(owner, manufacturer, model, classification, decoder)
    params = FilterParams(owner, manufacturer, model, classification, decoder)
    logging.warn(f"Params: {params}")
    return templates.TemplateResponse("roster.html", {"request": request, "roster_entries": entries, "filter_params": params})


@app.get("/roster_entry/{id}", response_class=HTMLResponse)
async def show_roster_entry(request: Request, id: str):
    entry = RosterDatabase().get_roster_entry_by_id(id)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Roster entry with id {id} not found")
    return templates.TemplateResponse("roster_entry.html", {"request": request, "roster_entry": entry})