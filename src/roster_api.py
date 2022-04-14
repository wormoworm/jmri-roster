from fastapi import FastAPI, HTTPException, Request, Response
import json
import os
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


@app.get("/api/v2/roster_entry/{id}/image")
def get_roster_entry_image(id: str, size: int = None):
    entry = RosterDatabase().get_roster_entry_by_id(id)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Roster entry with id {id} not found")
    try:
        with Image.open(f"{DIRECTORY_ROSTER}/{entry.image_file_path}") as image:
            width, height = image.size
            # TODO: Resize image if size is set
            logging.debug(f"Image size: {image.size}")
            image_bytes = BytesIO()
            image.save(image_bytes, format="jpeg")
            # media_type here sets the media type of the actual response sent to the client.
            return Response(content=image_bytes.getvalue(), media_type="image/jpeg")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Could not load image for roster entry with {id}: {str(e)}")

@app.get("/roster_entry/{id}", response_class=HTMLResponse)
async def show_roster_entry(request: Request, id: str):
    entry = RosterDatabase().get_roster_entry_by_id(id)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Roster entry with id {id} not found")
    return templates.TemplateResponse("roster_entry.html", {"request": request, "roster_entry": entry})